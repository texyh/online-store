$(document).ready(function(){

		$('.free').click(function(){
			$(this).toggleClass("green");
			$('.price').toggle(500);

		});

//handles the like button
 
		$('#like').click(function(){
			//alert($('body').css('color'))
			var id = $('#like').attr('value')
			if ($('.'+id).css('color') == $('.dummy').css('color') ){
				alert('you already liked')
			}else{
			
			like(id);
			
			}
		});


		$("#comment").click(function(){
			$('form').removeAttr('hidden');

		});

		$('.post-comment').click(function(event){
		var comment = $('.comment-box').val();
		var comm = $('#fc').html();
		$('.comments').prepend('<img class="img" src="http://res.cloudinary.com/onwuzulike/image/upload/v1476958065/ripple_nywlga.gif" />');
		$('.comments').append('<p>'+comment+'</p>');
		comm++; 
		$('#fc').html(comm);
		//$('.img').remove();

		$('.comment-box').val('');



		event.preventDefault();
		});


});

function like(id){
	$.ajax({
		data:{id:id},
		url:'/like',
		type:'POST'
	})
	.done(function(data){
		if (data=='yes'){
			$('.'+id).css('color','black');
			var clicks = $('.figure-'+id).html();
			clicks++; 
			$('.figure-'+id).html(clicks);
		}else{
			alert('Already liked this post')
		}
	})

};