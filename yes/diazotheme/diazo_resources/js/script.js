/* Author: 

*/

$(document).ready(function () {
    $('.field.error').each(function (idx, el) {
        if ($.trim($(el).text()) == '') {
            $(el).remove();
        }
    });
    // jQuery('.dropdown-toggle').click(function () {
    //     var self = $(this).parent();
    //     $('.dropdown.open').each(function (idx, item) {
    //         if ($(item)[0] != self[0]) {
    //             $(item).removeClass('open');
    //         }
    //     })
    // });

    jQuery('.carousel').carousel();

    // search button should work as search when field not collapsed
    $('#searchinput').on('hidden.bs.collapse', function () {
        $(this).next().attr('type', 'button');
    })

    $('#searchinput').on('hide.bs.collapse', function (e) {
        $('#nav li + li a').removeClass('narrow');
        $search = $(this).find('input');
        console.log($search.val());
        if ($search.val() != '') {
            $(this).parent('form').submit();
        }
    })

    $('#searchinput').on('show.bs.collapse', function () {
        $('#nav li a').addClass('narrow');
    })

})
