/* Author: 

*/
MutationObserver = window.MutationObserver || window.WebKitMutationObserver;

function prepPagination() {
  $("#pagination .active a").wrapInner('<span></span>');
  $("#pagination .active a").prepend('PAGE ');
  $("#pagination .active a").append(' OF '+$('#pagination').data("total-pages") );
}

/* adapted from http://stackoverflow.com/questions/8929177/getting-counts-for-twitter-links-facebook-likes-and-google-1-with-jquery-and-a */
function getfbcount(url){
     var fblikes;
     $.getJSON('http://graph.facebook.com/?ids=' + url, function(data){
        fblikes = data[url].shares;
        $('.f_facebook').html(fblikes);
     });
}

function gettwcount(url){
   var tweets;
   $.getJSON('http://urls.api.twitter.com/1/urls/count.json?url=' + url + '&callback=?', function(data){
      tweets = data.count;
      $('.f_twitter').html(tweets);
   });
}

function getplusone(url){
  $.ajax({
    type: 'GET',
    url: '@@googleplusones?page_url='+url,
  })
  .done(function (data){
    $('.f_plus').html(data);
  })
  .fail(function(){
  });
}

$(document).ready(function () {
    console.log('jquery document ready');
    $('.field.error').each(function (idx, el) {
        if ($.trim($(el).text()) === '') {
            $(el).remove();
        }
    });

    jQuery('.carousel').carousel();

    $('#pagination').twbsPagination({
        totalPages: $('#pagination').data("total-pages"),
        visiblePages: 1,
        href: 'javascript:void(0);',
        hrefVariable: 'Page {{number}}',
        first: 'First',
        prev: '&lt;',
        next: '&gt;',
        last: 'Last',
        onPageClick: function (event, page) {
            $('#content').html('Sample Lipsum');
            prepPagination();
        }
    });

    prepPagination();

    // get followers/likes/plusones
    var url = "http://www.yesmagazine.org";
    getfbcount(url);
    gettwcount(url);
    getplusone(url);

    // copy the above content sharebar to below content
    $('#below-content-sharebar').html($('#content-sharebar').html());

    $('.share').ShareLink({
      title: document.title,
      text: document.title,
      url: 'http://www.yesmagazine.org/happiness/an-astronomer-explains-why-this-is-the-best-moment-in-cosmic-history-to-be-alive'
    });
    $('.counter').ShareCounter({
      url: 'http://www.yesmagazine.org/happiness/an-astronomer-explains-why-this-is-the-best-moment-in-cosmic-history-to-be-alive'
    });

    // copy the right col. newsletter form to below content
    $('#below-newsletterform-holder').prepend($('#newsletterform form').clone());
    
});



function bindSearchInput() {
  console.log('binding search events');
  $('#searchinput').on('hidden.bs.collapse', function () {
      console.log('hidden.bs.collapse');
      $(this).next().attr('type', 'button');
  });

  $('#searchinput').on('hide.bs.collapse', function (e) {
      console.log('hide.bs.collapse');
      $('#nav li a').removeClass('narrow');
      $search = $(this).find('input');
      if ($search.val() !== '') {
          $(this).parent('form').submit();
      }
  });

  $('#searchinput').on('show.bs.collapse', function () {
      console.log('show.bs.collapse');
      $('#nav li a').addClass('narrow');
  });
}



Response.crossover(function(){
  bindSearchInput();
}, "width");


if (MutationObserver !== undefined) {

    var observer = new MutationObserver(function( mutations ) {
      mutations.forEach(function( mutation ) {
        var newNodes = mutation.addedNodes;
        if( newNodes !== null ) {
          var $nodes = $(newNodes).find('#searchinput');
          $nodes.each(function() {
            var $node = $(this);
            if( $node.is("#searchinput") ) {
              // we have our search input now
              // search button should work as search when field not collapsed
              bindSearchInput();
              observer.disconnect();
            }
          });
        }
      });
    });

    var config = {
      attributes: true,
      childList: true,
      characterData: true,
      subtree: true
    };
     
    observer.observe(window.document, config);

}

else {
    $(document).on("DOMNodeInserted", function (e) {
      //console.log(e.target);
      if (e.target.is('#searchinput')) {
        bindSearchInput();
        $(document).off("DOMNodeInserted");
      }
    });
}
