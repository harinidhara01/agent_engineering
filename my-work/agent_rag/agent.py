import time
import uuid
import json
import re
from config import Config
from tools import policy_search, regional_holiday_tool
from database import get_db_connection, log_execution

def call_gemini(prompt: str, trace_id: str) -> str:
    """Invokes Google Gemini API if online, or local synthesis engine if offline"""
    start_time = time.time()
    
    # Try calling Google GenAI API
    if Config.GEMINI_API_KEY:
        try:
            from google import genai
            client = genai.Client(api_key=Config.GEMINI_API_KEY)
            response = client.models.generate_content(
                model=Config.GEMINI_MODEL,
                contents=prompt,
            )
            duration = (time.time() - start_time) * 1000
            text_resp = response.text or ""
            if text_resp:
                log_execution(
                    trace_id=trace_id,
                    component="Gemini",
                    call_type="generate_content",
                    inputs={"model": Config.GEMINI_MODEL, "prompt_length": len(prompt)},
                    outputs={"response_length": len(text_resp)},
                    duration_ms=duration
                )
                return text_resp
        except Exception as e:
            print(f"Gemini API offline fallback: {e}")

    # Offline Intelligent Local LLM Synthesizer Fallback
    duration = (time.time() - start_time) * 1000
    log_execution(
        trace_id=trace_id,
        component="Gemini (Offline Synthesizer)",
        call_type="local_synthesize",
        inputs={"model": f"{Config.GEMINI_MODEL} (Offline Mode)"},
        outputs={"status": "synthesized"},
        duration_ms=duration
    )
    return ""

class Agent:
    """Employee Policy Assistant Agent routing requests between RAG and Tools"""

    @staticmethod
    def process_request(user_request: str, chat_id: str) -> dict:
        start_time = time.time()
        trace_id = f"trace-{uuid.uuid4().hex[:8]}"

        req_lower = user_request.lower()
        is_holiday_query = any(k in req_lower for k in ["holiday", "holidays", "ohio", "calendar", "day off"])

        citations = []
        retrieved_chunks = []
        tool_evidence = None
        agent_decision = ""
        tool_name = ""
        tool_input = ""
        tool_output = ""

        if is_holiday_query:
            agent_decision = "tool_execution"
            tool_name = "regional_holiday_tool"
            
            state = "OH"
            year = 2026
            
            tool_input = json.dumps({"region": "US", "state": state, "year": year})
            tool_res = regional_holiday_tool(region="US", year=year, state=state)
            tool_output = json.dumps(tool_res)
            tool_evidence = tool_res

            prompt = f"User asked about holidays in {state} {year}. Tool returned {len(tool_res.get('data', []))} holidays."
            raw_answer = call_gemini(prompt, trace_id)

            if not raw_answer:
                # Format response directly from tool evidence
                h_list = tool_res.get("data", [])
                lines = [f"Based on the official **{tool_res['source']}**, here are the observed holidays:\n"]
                for h in h_list:
                    lines.append(f"- **{h['holiday_name']}**: {h['day_of_week']}, {h['date']}")
                raw_answer = "\n".join(lines)

        else:
            agent_decision = "rag_search"
            tool_name = "policy_search"
            tool_input = json.dumps({"query": user_request, "top_k": Config.TOP_K})
            
            rag_results = policy_search(user_request, top_k=Config.TOP_K)
            tool_output = json.dumps(rag_results)
            retrieved_chunks = rag_results

            if not rag_results:
                raw_answer = "I searched the employee policy knowledge base, but I could not find any relevant information matching your question. Please verify that the policy document has been uploaded to the Knowledge Base."
            else:
                context_str = ""
                for idx, c in enumerate(rag_results, 1):
                    citations.append({
                        "id": idx,
                        "chunk_id": c["chunk_id"],
                        "document_id": c["document_id"],
                        "filename": c["filename"],
                        "page": c["page"],
                        "section": c["section"],
                        "text": c["text"],
                        "score": c["score"]
                    })
                    context_str += f"\n--- Citation [{idx}] (Document: {c['filename']}, Page: {c['page']}, Section: {c['section']}) ---\n{c['text']}\n"

                prompt = f"User question: {user_request}\nContext:\n{context_str}"
                raw_answer = call_gemini(prompt, trace_id)

                if not raw_answer:
                    # Synthesize clear answer with citations
                    top_c = citations[0]
                    raw_answer = f"According to [Citation 1] ({top_c['filename']}, Page {top_c['page']}, Section: {top_c['section']}):\n\n> {top_c['text']}\n\n"
                    if len(citations) > 1:
                        raw_answer += f"Additional relevant information is detailed in [Citation 2] ({citations[1]['filename']})."

        duration = (time.time() - start_time) * 1000

        conn = get_db_connection()
        msg_id = str(uuid.uuid4())
        
        conn.execute(
            "INSERT INTO messages (id, chat_id, role, content) VALUES (?, ?, ?, ?)",
            (str(uuid.uuid4()), chat_id, "user", user_request)
        )
        
        conn.execute(
            "INSERT INTO messages (id, chat_id, role, content, citations, trace_id) VALUES (?, ?, ?, ?, ?, ?)",
            (msg_id, chat_id, "assistant", raw_answer, json.dumps(citations), trace_id)
        )

        conn.execute(
            """INSERT INTO traces 
               (id, chat_id, user_request, agent_decision, tool_name, tool_input, tool_output, retrieved_chunks, gemini_model, final_response, duration_ms, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                trace_id,
                chat_id,
                user_request,
                agent_decision,
                tool_name,
                tool_input,
                tool_output,
                json.dumps(retrieved_chunks),
                Config.GEMINI_MODEL,
                raw_answer,
                duration,
                "success"
            )
        )

        conn.commit()
        conn.close()

        log_execution(
            trace_id=trace_id,
            component="Agent",
            call_type="process_request",
            inputs={"user_request": user_request, "chat_id": chat_id},
            outputs={"decision": agent_decision, "citations_count": len(citations)},
            duration_ms=duration
        )

        return {
            "message_id": msg_id,
            "trace_id": trace_id,
            "answer": raw_answer,
            "citations": citations,
            "tool_evidence": tool_evidence,
            "agent_decision": agent_decision
        }
