document.addEventListener('DOMContentLoaded', function () {
    
  let currentSlide = 1;
  let numOfSlides = 4;
  let inTransition = true;

  // from:
  // --     -> active right -> active -> active left  -> --
  // to:
  // active -> active left  -> --     -> active right -> active
  //        1               2         3               4
  function changeSlides() {
        
    let nextSlide = (currentSlide % numOfSlides) + 1;
    var slideToChangeFrom = document.getElementById('slide' + currentSlide);
    var slideToChangeTo = document.getElementById('slide' + nextSlide);
            
    // 4
    if (slideToChangeTo.classList.contains('active', 'right')) {
        
        slideToChangeFrom.classList.remove('active', 'left');
        void slideToChangeTo.offsetWidth;
        slideToChangeTo.classList.remove('right');
        currentSlide += 1;
        if (currentSlide == numOfSlides + 1) currentSlide = 1;
        inTransition = true;
    }

    // 2
    else if (slideToChangeTo.classList.contains('active', 'left')) {
                
        slideToChangeTo.classList.remove('active', 'left');
        void slideToChangeFrom.offsetWidth;
        slideToChangeFrom.classList.remove('right');
        inTransition = true;
    }

    // 3
    else if (slideToChangeFrom.classList.contains('active')) {
          
        slideToChangeTo.classList.add('active', 'right');
        slideToChangeFrom.classList.add('left');
        inTransition = false;
    }

    // 1
    else if (slideToChangeTo.classList.contains('active')) {
                
        slideToChangeTo.classList.add('left');
        slideToChangeFrom.classList.add('active', 'right');
        inTransition = false;
    }

  }

  function showSlide(slideNumber) {

    // Hide all slides
    document.querySelectorAll('.slide').forEach(function (slide) {
    
      slide.classList.remove('active', 'left', 'right');
     
    });

    // Show the selected slide
    document.getElementById('slide' + slideNumber)
     
      .classList.add('active');
      
  }

  function transition() {
  
    // 3000 milliseconds for states 1 and 3
    if (!inTransition) {
    
      changeSlides();
      timeout = setTimeout(transition, 4000);
      
    }
    
    // 200 milliseconds for states 2 and 4
    else {
  
      changeSlides();
      timeout = setTimeout(transition, 500);
      
    }
    
  }


  // Event listener for navigation circles
  document.querySelectorAll('.circle').forEach(function (circle) {
  
    circle.addEventListener('click', function () {
    
      currentSlide = parseInt(circle.dataset.slide);
      showSlide(currentSlide);
      
    });
    
  });
              
  transition()
});
