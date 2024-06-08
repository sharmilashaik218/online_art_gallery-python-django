
$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];
    console.log("pid=",id);

    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            art_id: id
        },
        success: function(data) {
            console.log("data=", data);
            eml.innerText = data.quantity;
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
        }
    });
});

$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];
    console.log("pid=", id);

    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            art_id: id
        },
        success: function(data) {
            console.log("data=", data);
            eml.innerText = data.quantity;
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
        }
    });
});


$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this;

    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            art_id: id
        },
        success: function(data) {
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
            eml.closest('.row').remove(); // Use closest to find the closest ancestor with the 'row' class and remove it
        }
    });
});
