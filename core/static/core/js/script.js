// Initialize AOS
// AOS.init is already called in base.html, but we can keep custom logic here if needed.

document.addEventListener('DOMContentLoaded', () => {
  // GSAP ScrollTrigger Registration
  gsap.registerPlugin(ScrollTrigger);

  // Hero Section Animation
  gsap.from(".hero-section h1", {
    duration: 1,
    y: 50,
    opacity: 0,
    ease: "power3.out",
    delay: 0.5
  });

  gsap.from(".hero-section p", {
    duration: 1,
    y: 30,
    opacity: 0,
    ease: "power3.out",
    delay: 0.8
  });

  gsap.from(".hero-section .btn", {
    duration: 1,
    y: 20,
    opacity: 0,
    ease: "power3.out",
    delay: 1,
    stagger: 0.2
  });

  /* 
  // Staggered Entry for Cards - Commented out to prevent conflict with AOS
  const sections = document.querySelectorAll('.section-padding');

  sections.forEach(section => {
    const cards = section.querySelectorAll('.glass-card, .project-card');

    if (cards.length > 0) {
      gsap.from(cards, {
        scrollTrigger: {
          trigger: section,
          start: "top 80%",
          toggleActions: "play none none reverse"
        },
        y: 50,
        opacity: 0,
        duration: 0.8,
        stagger: 0.1,
        ease: "power2.out"
      });
    }
  });
  */


  // Navbar Glass Effect on Scroll
  const navbar = document.querySelector('.navbar');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  });

  // Agent Terminal Typing Effect
  const terminalContent = document.getElementById('terminal-content');
  if (terminalContent) {
    const commands = [
      { text: "> initializing_agent_core...", delay: 500 },
      { text: "> loading_modules: [NLP, Vision, Predictive]", delay: 1500 },
      { text: "> connecting_to_neural_net...", delay: 2500 },
      { text: "> status: ONLINE", delay: 3500, class: "text-primary" },
      { text: "> awaiting_input...", delay: 4500 }
    ];

    let currentCommandIndex = 0;

    function typeCommand(command) {
      const line = document.createElement('div');
      line.className = `mb-2 ${command.class || ''}`;
      terminalContent.appendChild(line);

      let i = 0;
      const typeInterval = setInterval(() => {
        line.textContent += command.text.charAt(i);
        i++;
        if (i >= command.text.length) {
          clearInterval(typeInterval);
          currentCommandIndex++;
          if (currentCommandIndex < commands.length) {
            setTimeout(() => typeCommand(commands[currentCommandIndex]), 500);
          }
        }
      }, 30); // Typing speed
    }

    setTimeout(() => typeCommand(commands[0]), 1000);
  }
});
