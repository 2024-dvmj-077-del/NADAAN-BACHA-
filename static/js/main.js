(() => {
  const $ = (s) => document.querySelector(s);
  const scenes = [...document.querySelectorAll('.scene')];
  const music = $('#backgroundMusic');
  const meow = $('#meow');
  let greetingTimer = null;
  let musicStarted = false;

  function stopMeow() { if (meow) { meow.pause(); meow.currentTime = 0; } }
  function startMusic() {
    if (!music || musicStarted) return;
    musicStarted = true;
    music.volume = 0.34;
    music.play().catch(() => { musicStarted = false; });
  }
  function startGreeting() {
    const speech = $('#speech');
    const note = $('#deliveryNote');
    const cat = $('.courier-gif');
    if (!speech || !note) return;
    speech.classList.remove('show'); note.classList.remove('show');
    cat?.classList.remove('cat-exit');
    clearTimeout(greetingTimer); stopMeow();
    speech.textContent = '';
    greetingTimer = setTimeout(() => {
      speech.classList.add('show');
      meow?.play().catch(() => {});
      const words = ['Hi,', 'Nadaan', 'Bachcha!', 'Look', 'what', 'I', 'brought', 'for', 'you. ♡'];
      let i = 0;
      const typing = setInterval(() => {
        speech.textContent += (i ? ' ' : '') + words[i];
        i += 1;
        if (i >= words.length) {
          clearInterval(typing);
          setTimeout(() => {
            cat?.classList.add('cat-exit');
            stopMeow();
            setTimeout(() => note.classList.add('show'), 650);
          }, 900);
        }
      }, 360);
    }, 850);
  }
  function showScene(id) {
    scenes.forEach(s => s.classList.toggle('active', s.id === id));
    window.scrollTo({top:0,behavior:'smooth'});
    if (id === 'delivery') startGreeting(); else stopMeow();
    if (id === 'sher') prepareSherVoice();
  }
  document.querySelectorAll('[data-next]').forEach(btn => btn.addEventListener('click', () => {
    startMusic(); showScene(btn.dataset.next);
  }));
  $('#themeToggle')?.addEventListener('click', () => {
    document.body.classList.toggle('dark');
    $('#themeToggle').textContent = document.body.classList.contains('dark') ? '☀' : '☾';
  });
  $('#musicToggle')?.addEventListener('click', async () => {
    if (music.paused) { startMusic(); try { await music.play(); musicStarted = true; } catch (_) {} }
    else music.pause();
    $('#musicToggle').textContent = music.paused ? '♫' : 'Ⅱ';
  });
  $('#restart')?.addEventListener('click', () => {
    stopMeow(); if (music) { music.pause(); music.currentTime = 0; musicStarted = false; }
    showScene('cover');
  });
  function prepareSherVoice() {
    const audio = $('#sherVoice');
    if (!audio) return;
    fetch('./static/audio/sher-voice.m4a', {method:'HEAD'}).then(r => {
      if (r.ok) { audio.src='./static/audio/sher-voice.m4a'; audio.hidden=false; $('#voiceStatus').textContent='Voice recording ready.'; }
    }).catch(()=>{});
  }
  const lines = [...document.querySelectorAll('.sher-card p')];
  const syncLines = () => {
    const audio = $('#sherVoice');
    if (!audio || !audio.src || !window.SHER_LINE_TIMES) return;
    const t = audio.currentTime;
    let active = -1;
    window.SHER_LINE_TIMES.forEach((start,i)=>{ if (t >= start) active=i; });
    lines.forEach((line,i)=>line.classList.toggle('line-active',i===active));
  };
  $('#sherVoice')?.addEventListener('timeupdate', syncLines);
  showScene('cover');
  startMusic();
})();
