(function ($) {
    "use strict";

    /* TOP Menu Sticky */
    $(window).on('scroll', function () {
        const scroll = $(window).scrollTop();
        if (scroll < 400) {
            $("#sticky-header").removeClass("sticky");
            $('#back-top').fadeIn(500);
        } else {
            $("#sticky-header").addClass("sticky");
            $('#back-top').fadeIn(500);
        }
    });

    $(document).ready(function () {

        /* magnificPopup video view */
        $('.popup-video').magnificPopup({
            type: 'iframe'
        });

        /* review-active */
        $('.slider_active').owlCarousel({
            loop: true,
            margin: 0,
            items: 1,
            autoplay: true,
            navText: ['<i class="ti-angle-left"></i>', '<i class="ti-angle-right"></i>'],
            nav: true,
            dots: false,
            autoplayHoverPause: true,
            autoplaySpeed: 800,
            responsive: {
                0: {
                    items: 1, nav: false,
                }, 767: {
                    items: 1, nav: false,
                }, 992: {
                    items: 1
                }
            }
        });

        /* counter */
        $('.counter').counterUp({
            delay: 10, time: 10000
        });

    });

})(jQuery);