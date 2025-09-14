document.addEventListener('DOMContentLoaded', function(){
  document.querySelectorAll('form').forEach(function(f){
    f.addEventListener('submit', function(){
      const btn = f.querySelector('button[type="submit"]');
      if(btn){ btn.disabled = true; }
    });
  });
});
