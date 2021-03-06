$(function() {
  $('#nav').spasticNav({select: '.porfolio'});

  $('.ad-thumb-list>li.picture').each(function(){
    var $this = $(this);
    $this.find('img').data('ad-desc', $this.find('.picture_data').html());
  });
    
  var galleries = $('.ad-gallery').adGallery({
    update_window_hash: true,
    description_wrapper: $('.ad-image-description'),
    callbacks: {
      afterImageVisible: function(){
        // preload next image
        var context = this;
        this.preloadImage(this.current_index + 1);
        $('.ad-image>img').click(function(){
          window.location.href = $(this).attr('src');
        });
      }
    }
  });
  
  $('#switch-effect').change(
    function() {
      galleries[0].settings.effect = $(this).val();
      return false;
    }
  );
  $('#toggle-slideshow').click(
    function() {
      galleries[0].slideshow.toggle();
      return false;
    }
  );
  $('#toggle-description').click(
    function() {
      if(!galleries[0].settings.description_wrapper) {
        galleries[0].settings.description_wrapper = $('#descriptions');
      } else {
        galleries[0].settings.description_wrapper = false;
      }
      return false;
    }
  );
});

