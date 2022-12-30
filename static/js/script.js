function add_or_remove_favorite(element) {
    let productID = element.data('product'),
        heart = element.find('svg.bi-heart'),
        heartFill = element.find('svg.bi-heart-fill');

    $.get(`/ajax-favorites/${productID}/`, function (data) {
        if (data.created === true) {
            heart.addClass('d-none')
            heartFill.removeClass('d-none')
        } else {
            heartFill.addClass('d-none')
            heart.removeClass('d-none')
        }
    }).fail(function (error) {
        console.log(error);
    });
}