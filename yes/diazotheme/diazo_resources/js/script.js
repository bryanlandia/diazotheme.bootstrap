/* Author: 

*/
MutationObserver = window.MutationObserver || window.WebKitMutationObserver;


$(document).ready(function () {
    console.log('jquery document ready');
    $('.field.error').each(function (idx, el) {
        if ($.trim($(el).text()) == '') {
            $(el).remove();
        }
    });

    jQuery('.carousel').carousel();

});



function bindSearchInput() {
  console.log('binding search events');
  $('#searchinput').on('hidden.bs.collapse', function () {
      console.log('hidden.bs.collapse');
      $(this).next().attr('type', 'button');
  })

  $('#searchinput').on('hide.bs.collapse', function (e) {
      console.log('hide.bs.collapse');
      $('#nav li a').removeClass('narrow');
      $search = $(this).find('input');
      if ($search.val() != '') {
          $(this).parent('form').submit();
      }
  })

  $('#searchinput').on('show.bs.collapse', function () {
      console.log('show.bs.collapse');
      $('#nav li a').addClass('narrow');
  })
}



Response.crossover(function(){
  bindSearchInput();
}, "width");


if (MutationObserver != undefined) {

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
    })
}

