function add_or_remove_favorite(element) {
    let productID = element.data('product'),
        heart = element.find('svg.bi-heart'),
        heartFill = element.find('svg.bi-heart-fill');
    $.get(`ajax-favorites/${productID}/`, function (data) {
        console.log(data.created)
        if (data.created === true) {
            heart.addClass('d-none')
            heartFill.removeClass('d-none')
            // console.log('1')
            // console.log(heart)
            // console.log(heartFill)
        } else {
            heartFill.addClass('d-none')
            heart.removeClass('d-none')
            // console.log('2')
            // console.log(heart)
            // console.log(heartFill)
        }
    }).fail(function (error) {
        console.log(error);
    });
}