<?php
/**
 * Site chrome — global header + footer + Divi override layer.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

// Editable primary menu.
add_action( 'after_setup_theme', function () {
	register_nav_menu( 'tb_primary', 'Templeton Built — Primary' );
} );

function tb_nav_items() {
	if ( has_nav_menu( 'tb_primary' ) ) {
		$items = wp_get_nav_menu_items( get_nav_menu_locations()['tb_primary'] );
		if ( $items ) {
			$out = '';
			foreach ( $items as $i ) {
				$cur = ( untrailingslashit( $i->url ) === untrailingslashit( home_url( add_query_arg( array() ) ) ) ) ? ' aria-current="page"' : '';
				$out .= '<a href="' . esc_url( $i->url ) . '"' . $cur . '>' . esc_html( $i->title ) . '</a>';
			}
			return $out;
		}
	}
	$fallback = array(
		'/projects'     => 'Projects',
		'/custom-homes' => 'Custom homes',
		'/extensions'   => 'Extensions',
		'/renovations'  => 'Renovations',
		'/open-book'    => 'Open book',
		'/about'        => 'About',
		'/journal'      => 'Journal',
	);
	$out = '';
	$here = untrailingslashit( home_url( add_query_arg( array() ) ) );
	foreach ( $fallback as $path => $label ) {
		$url = home_url( $path );
		$cur = ( untrailingslashit( $url ) === $here ) ? ' aria-current="page"' : '';
		$out .= '<a href="' . esc_url( $url ) . '"' . $cur . '>' . esc_html( $label ) . '</a>';
	}
	return $out;
}

/** True on pages that should render bare (ad landing pages + thank-you). */
function tb_is_bare() {
	if ( ! is_page() ) { return false; }
	$slug = get_post_field( 'post_name', get_queried_object_id() );
	return ( 0 === strpos( $slug, 'lp-' ) || 'thank-you' === $slug );
}

/** Header — dark/transparent over hero pages, solid elsewhere. */
add_action( 'wp_body_open', function () {
	if ( tb_is_bare() ) {
		?>
		<header class="lp-nav">
		  <div class="wrap lp-nav-in">
		    <a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="logo">
		      <img src="https://templetonbuilt.com.au/wp-content/uploads/2025/05/Templeton-Logo.png" alt="Templeton Built">
		    </a>
		    <a href="tel:1800955111" class="lp-phone">1800 955 111</a>
		  </div>
		</header>
		<?php
		return;
	}
	// Pages whose first section is a dark hero get the transparent-over treatment.
	$over = is_front_page() || is_singular();
	?>
	<nav class="nav<?php echo $over ? ' over' : ''; ?>" id="nav">
	  <div class="wrap nav-in">
	    <a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="logo" aria-label="Templeton Built home">
	      <img src="https://templetonbuilt.com.au/wp-content/uploads/2025/05/Templeton-Logo.png" alt="Templeton Built" width="170" height="34">
	    </a>
	    <button class="nav-toggle" id="toggle" aria-label="Open menu" aria-expanded="false">
	      <svg width="26" height="14" viewBox="0 0 26 14" fill="none" aria-hidden="true"><path d="M0 1h26M0 13h26" stroke="currentColor" stroke-width="1.4"/></svg>
	    </button>
	    <div class="nav-links" id="links">
	      <?php echo tb_nav_items(); ?>
	      <a href="<?php echo esc_url( home_url( '/contact' ) ); ?>" class="nav-cta">Start a conversation</a>
	    </div>
	  </div>
	</nav>
	<?php
}, 5 );

/** Footer. */
add_action( 'wp_footer', function () {
	$h = function ( $p ) { return esc_url( home_url( $p ) ); };
	if ( tb_is_bare() ) {
		?>
		<footer class="foot"><div class="wrap"><div class="foot-base" style="border:0;padding:34px 0">
		  <span>&copy; Templeton Built Pty Ltd &middot; ABN 16 067 209 161 &middot; Licence BLD183145</span>
		  <span>12 Stirling Street, Thebarton SA 5033</span>
		</div></div></footer>
		<?php
		return;
	}
	?>
	<footer class="foot" id="contact-foot">
	  <div class="wrap">
	    <div class="foot-top">
	      <div class="rev">
	        <span class="label">Get in touch</span>
	        <h2 style="margin-top:22px">Tell us what you're thinking of building.</h2>
	      </div>
	      <div class="foot-contact rev">
	        <a href="tel:1800955111" class="big">1800 955 111</a>
	        <a href="mailto:hello@templetonbuilt.com.au" class="big">hello@templetonbuilt.com.au</a>
	        <p style="color:rgba(251,250,248,.72);margin:0">12 Stirling Street, Thebarton SA 5033<br>Monday&ndash;Friday, 7am&ndash;4pm</p>
	        <a href="<?php echo $h( '/contact' ); ?>" class="btn btn-light">Book a site conversation</a>
	      </div>
	    </div>
	    <div class="foot-cols">
	      <div><h4>What we build</h4><ul>
	        <li><a href="<?php echo $h( '/custom-homes' ); ?>">Custom homes</a></li>
	        <li><a href="<?php echo $h( '/extensions' ); ?>">Extensions</a></li>
	        <li><a href="<?php echo $h( '/renovations' ); ?>">Renovations</a></li>
	      </ul></div>
	      <div><h4>Studio</h4><ul>
	        <li><a href="<?php echo $h( '/about' ); ?>">About Templeton Built</a></li>
	        <li><a href="<?php echo $h( '/open-book' ); ?>">The open book</a></li>
	        <li><a href="<?php echo $h( '/projects' ); ?>">Projects</a></li>
	        <li><a href="<?php echo $h( '/journal' ); ?>">Journal</a></li>
	      </ul></div>
	      <div><h4>Start here</h4><ul>
	        <li><a href="<?php echo $h( '/architect-guide' ); ?>">Before you brief an architect</a></li>
	        <li><a href="<?php echo $h( '/cost-benchmark' ); ?>">Adelaide cost benchmark</a></li>
	        <li><a href="<?php echo $h( '/contact' ); ?>">Book a conversation</a></li>
	      </ul></div>
	      <div><h4>Details</h4><ul>
	        <li>ABN 16 067 209 161</li>
	        <li>Licence BLD183145</li>
	        <li><a href="https://www.instagram.com/templetonbuilt.au" rel="noopener">Instagram</a></li>
	        <li><a href="https://www.facebook.com/templetonbuilt.au/" rel="noopener">Facebook</a></li>
	      </ul></div>
	    </div>
	    <div class="foot-base">
	      <span>&copy; Templeton Built Pty Ltd <?php echo esc_html( gmdate( 'Y' ) ); ?></span>
	      <span>Adelaide, South Australia</span>
	    </div>
	  </div>
	</footer>
	<?php
}, 5 );

/** Divi override layer — Divi's content styles outrank the design system on lists. */
add_action( 'wp_head', function () { ?>
<style id="tb-divi-overrides">
.et_pb_code ul,.et_pb_code ol,.foot ul{list-style:none!important;padding-left:0!important}
.et_pb_code .prose ul,.et_pb_code .prose ol{list-style:disc!important;padding-left:1.2em!important}
.et_pb_code .prose ol{list-style:decimal!important}
.et_pb_code li{margin:0}
.et_pb_code .prose li{margin-bottom:.5em}
.et_pb_code a{transition:none}
.et_pb_section,.et_pb_row,.et_pb_column,.et_pb_module{margin:0!important}
.et_pb_row{padding:0!important;width:100%!important;max-width:none!important}
.et_pb_code img{max-width:100%;height:auto}
#page-container{padding-top:0!important;margin-top:0!important}
.et_pb_code .check li{padding:2.6mm 0 2.6mm 8mm}
.person img{filter:none!important}
</style>
<?php }, 99 );
