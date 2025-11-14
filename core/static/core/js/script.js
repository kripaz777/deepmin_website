// core/static/core/js/script.js
document.addEventListener('DOMContentLoaded', function () {
  // AOS init
  if(window.AOS) AOS.init({ duration: 900, once: true });

  // Typed loop for hero
  const phrases = [
    "Develop, Operate & Deploy AI You Can Trust at Scale",
    "Turn Data into High-Value AI Outcomes",
    "Build Reliable AI Workflows for Production",
    "Train Teams, Ship Models, Operate at Scale"
  ];
  let pIndex=0, lIndex=0, deleting=false;
  const typedEl = document.getElementById('typed-text');
  if(typedEl){
    const tick = () => {
      const current = phrases[pIndex % phrases.length];
      if(!deleting){
        typedEl.textContent = current.substring(0, ++lIndex);
        if(lIndex === current.length){ deleting = true; setTimeout(tick, 1400); return; }
      } else {
        typedEl.textContent = current.substring(0, --lIndex);
        if(lIndex === 0){ deleting = false; pIndex++; setTimeout(tick, 400); return; }
      }
      setTimeout(tick, deleting ? 40 : 90);
    };
    tick();
  }

  // Counters
  const counters = document.querySelectorAll('.stat-num');
  const counterObserver = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if(entry.isIntersecting){
        const el = entry.target;
        const target = parseInt(el.dataset.target || el.getAttribute('data-target') || el.textContent) || 0;
        let start = 0;
        const step = Math.max(1, Math.floor(target / 60));
        const run = () => {
          start += step;
          if(start >= target) { el.textContent = target; }
          else { el.textContent = start; requestAnimationFrame(run); }
        };
        run();
        obs.unobserve(el);
      }
    });
  }, { threshold: 0.6 });
  counters.forEach(c => counterObserver.observe(c));

  // Workflow reveal
  const workflowSteps = document.querySelectorAll('.workflow-step');
  if(workflowSteps.length){
    const stepObserver = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if(entry.isIntersecting){
          entry.target.classList.add('reveal');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });
    workflowSteps.forEach(s => stepObserver.observe(s));
  }

  // Back to top
  const back = document.getElementById('backToTop');
  if(back){
    window.addEventListener('scroll', () => {
      if(window.scrollY > 400) back.style.display = 'flex';
      else back.style.display = 'none';
    });
    back.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

  // Throttle Lottie on small devices
  try {
    const players = document.querySelectorAll('lottie-player');
    const small = /Mobi|Android/i.test(navigator.userAgent) && window.innerWidth < 600;
    if(small){
      players.forEach(p => { try { p.pause(); } catch(e){} });
      const workflowSection = document.getElementById('workflows');
      if(workflowSection){
        const resumeObserver = new IntersectionObserver((entries, obs) => {
          entries.forEach(entry => {
            if(entry.isIntersecting){
              players.forEach(p => { try { p.play(); } catch(e){} });
              obs.disconnect();
            }
          });
        }, { threshold: 0.25 });
        resumeObserver.observe(workflowSection);
      }
    }
  } catch (e) { console.warn('Lottie throttle error', e); }

  // Demo subscribe form
  const sub = document.getElementById('subscribeForm');
  if(sub){
    sub.addEventListener('submit', e => { e.preventDefault(); alert('Thanks — subscription recorded (demo).'); sub.reset(); });
  }
});
