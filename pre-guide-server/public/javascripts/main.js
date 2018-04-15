$(document).ready(
	function() {
		$('#example').DataTable({
			searching: false,
			lengthChange: false,
			pageLength: 5,
			pagingType: 'full'
		});

		d = document;
		s = 'script';
		id = 'facebook-jssdk';
		var js, fjs = d.getElementsByTagName(s)[0];
		if (d.getElementById(id)) return;
		js = d.createElement(s); js.id = id;
		js.src = 'https://connect.facebook.net/en_GB/sdk.js#xfbml=1&version=v2.12';
		fjs.parentNode.insertBefore(js, fjs);
	}
);