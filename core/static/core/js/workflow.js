
document.addEventListener('DOMContentLoaded', () => {
    // Check if GSAP is loaded
    if (typeof gsap === 'undefined') {
        console.error('GSAP not loaded');
        return;
    }

    const workflowContainer = document.querySelector('.agent-workflow');
    if (!workflowContainer) return;

    // IMPORTANT: Register the plugin!
    if (typeof MotionPathPlugin !== 'undefined') {
        gsap.registerPlugin(MotionPathPlugin);
    } else {
        console.warn('GSAP MotionPathPlugin not found');
    }

    // Animation Sequence
    const masterTimeline = gsap.timeline({ repeat: -1, repeatDelay: 2 });

    // Node Selectors
    const nodes = {
        source: document.querySelector('.node-source'),
        scraper: document.querySelector('.node-scraper'),
        cleaner: document.querySelector('.node-cleaner'),
        training: document.querySelector('.node-training'),
        kb: document.querySelector('.node-kb'),
        agent: document.querySelector('.node-agent'),
        chat: document.querySelector('.node-chat')
    };

    // Helper for node pulse
    const pulseNode = (node, color) => {
        return gsap.to(node, {
            boxShadow: `0 0 20px ${color}`,
            scale: 1.1,
            borderColor: color,
            duration: 0.4,
            yoyo: true,
            repeat: 1
        });
    };

    // 1. Source -> Scraper
    const packet1 = document.querySelector('.packet-1');
    masterTimeline.add(pulseNode(nodes.source, '#ffffff'));

    if (packet1) {
        masterTimeline.to(packet1, {
            motionPath: {
                path: "#path-1",
                align: "#path-1",
                alignOrigin: [0.5, 0.5],
                autoRotate: true
            },
            duration: 1,
            ease: "power1.inOut",
            opacity: 1
        });
    }

    // 2. Scraper Process + Move to Cleaner
    masterTimeline.add(pulseNode(nodes.scraper, '#00e5ff'), "-=0.2");

    const packet2 = document.querySelector('.packet-2');
    if (packet2) {
        masterTimeline.to(packet2, {
            motionPath: {
                path: "#path-2",
                align: "#path-2",
                alignOrigin: [0.5, 0.5],
                autoRotate: true
            },
            duration: 1,
            ease: "power1.inOut",
            opacity: 1
        });
    }

    // 3. Cleaner Process + Move to Training
    masterTimeline.add(pulseNode(nodes.cleaner, '#00f260'), "-=0.2");

    const packet3 = document.querySelector('.packet-3');
    if (packet3) {
        masterTimeline.to(packet3, {
            motionPath: {
                path: "#path-3",
                align: "#path-3",
                alignOrigin: [0.5, 0.5],
                autoRotate: true
            },
            duration: 1,
            ease: "power1.inOut",
            opacity: 1
        });
    }

    // 4. Training Process (Longer) + Move to KB
    masterTimeline.add(gsap.to(nodes.training, {
        boxShadow: "0 0 30px #a0aec0",
        scale: 1.15,
        duration: 0.6,
        yoyo: true,
        repeat: 3
    }), "-=0.2");

    const packet4 = document.querySelector('.packet-4');
    if (packet4) {
        masterTimeline.to(packet4, {
            motionPath: {
                path: "#path-4",
                align: "#path-4",
                alignOrigin: [0.5, 0.5],
                autoRotate: true
            },
            duration: 1,
            ease: "power1.inOut",
            opacity: 1
        });
    }

    // 5. KB -> Agent (Context Retrieval)
    masterTimeline.add(pulseNode(nodes.kb, '#ffd700'), "-=0.2");

    const packet5 = document.querySelector('.packet-5');
    if (packet5) {
        masterTimeline.to(packet5, {
            motionPath: {
                path: "#path-5",
                align: "#path-5",
                alignOrigin: [0.5, 0.5],
                autoRotate: true
            },
            duration: 0.8,
            ease: "power1.out",
            opacity: 1
        });
    }

    // 6. Agent Thinking + Response to Chat
    masterTimeline.add(pulseNode(nodes.agent, '#ff0055'), "-=0.2");

    const packet6 = document.querySelector('.packet-6');
    if (packet6) {
        masterTimeline.to(packet6, {
            motionPath: {
                path: "#path-6",
                align: "#path-6",
                alignOrigin: [0.5, 0.5],
                autoRotate: true
            },
            duration: 0.8,
            ease: "power1.out",
            opacity: 1
        });
    }

    // 7. Chat Interface Receives
    masterTimeline.add(gsap.to(nodes.chat, {
        boxShadow: "0 0 25px #ffffff",
        borderColor: "#ffffff",
        y: -5,
        duration: 0.5,
        yoyo: true,
        repeat: 1
    }), "-=0.1");

    // Show typed message effect simulation in chat
    const typewriterElement = document.querySelector('.typewriter-text');
    if (typewriterElement) {
        masterTimeline.to(typewriterElement, {
            text: { value: "> using offline models in ollama" }, // requires TextPlugin but we can fallback or use simple replace
            duration: 1.5,
            delay: 0.2,
            onStart: function () { this.targets()[0].innerText = "> "; }, // Clear before typing
            onUpdate: function () {
                const progress = this.progress();
                const str = "> using offline models in ollama";
                const len = Math.floor(progress * str.length);
                this.targets()[0].innerText = str.substring(0, len);
            }
        });
    }

    // Reset loop
    masterTimeline.to([packet1, packet2, packet3, packet4, packet5, packet6], { opacity: 0, duration: 0.1 });
    if (typewriterElement) {
        masterTimeline.set(typewriterElement, { innerText: "> awaiting_input..." });
    }
});
