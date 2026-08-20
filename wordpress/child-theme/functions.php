<?php
/**
 * Templeton Built — Divi child theme
 */

// Parent + child stylesheets
add_action( 'wp_enqueue_scripts', function () {
	wp_enqueue_style( 'divi-parent-style', get_template_directory_uri() . '/style.css' );
	wp_enqueue_style(
		'templeton-child-style',
		get_stylesheet_directory_uri() . '/style.css',
		array( 'divi-parent-style' ),
		wp_get_theme()->get( 'Version' )
	);
}, 20 );

// Google Fonts — Archivo (display/labels) + Newsreader (body)
add_action( 'wp_head', function () {
	echo '<link rel="preconnect" href="https://fonts.googleapis.com">' . "\n";
	echo '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' . "\n";
	echo '<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300;1,6..72,400&display=swap" rel="stylesheet">' . "\n";
}, 1 );

// Scroll-reveal + sticky nav behaviour used by the design system
add_action( 'wp_footer', function () { ?>
<script>
(function(){
  var nav=document.getElementById('nav');
  if(nav){
    var s=function(){nav.classList.toggle('solid',window.scrollY>60)};
    s();window.addEventListener('scroll',s,{passive:true});
    var t=document.getElementById('toggle'),l=document.getElementById('links');
    if(t&&l){
      t.addEventListener('click',function(){
        var o=l.classList.toggle('open');
        t.classList.toggle('open',o);t.setAttribute('aria-expanded',o);
      });
    }
  }
  var r=document.querySelectorAll('.rev');
  if(!r.length)return;
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){
    r.forEach(function(e){e.classList.add('in')});return;
  }
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})
  },{threshold:.12,rootMargin:'0px 0px -8% 0px'});
  r.forEach(function(e){io.observe(e)});
})();
</script>
<?php }, 20 );
