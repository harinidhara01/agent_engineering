document.addEventListener('DOMContentLoaded', () => {
    // Only run on the processing page
    if (document.querySelector('.processing-container')) {
        simulateWorkflow();
    }
});

async function simulateWorkflow() {
    const steps = [
        'step-1',
        'step-2',
        'step-3',
        'step-4'
    ];
    
    // Simulate sequential steps visually
    for (let i = 0; i < steps.length; i++) {
        await new Promise(r => setTimeout(r, 600)); // wait for effect
        document.getElementById(steps[i]).classList.replace('pending', 'done');
    }
    
    // Show parallel stage
    document.getElementById('parallel-stage').classList.remove('hidden');
    
    // Wait a bit
    await new Promise(r => setTimeout(r, 800));
    
    // Simulate parallel completion
    const provs = ['prov-1', 'prov-2', 'prov-3', 'prov-4'];
    provs.forEach(p => {
        document.getElementById(p).classList.replace('pending', 'done');
    });
    
    // Show ranking stage
    document.getElementById('ranking-stage').classList.remove('hidden');
    await new Promise(r => setTimeout(r, 600));
    document.getElementById('step-rank').classList.replace('pending', 'done');
    
    // Now actually trigger the backend processing
    try {
        const response = await fetch('/api/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            window.location.href = '/recommendations';
        } else {
            document.getElementById('error-message').textContent = data.error || 'An error occurred during processing.';
            document.getElementById('error-message').classList.remove('hidden');
            if (data.missing) {
                document.getElementById('error-message').textContent += ' Missing: ' + data.missing.join(', ');
            }
        }
    } catch (err) {
        document.getElementById('error-message').textContent = 'Network error during processing.';
        document.getElementById('error-message').classList.remove('hidden');
    }
}
