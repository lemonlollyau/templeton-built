<?php
/**
 * Plugin Name: Templeton Built — Site Content
 * Description: Installs the Templeton Built page structure, Divi layouts, Rank Math meta and 301 redirect map. Run from Tools → Templeton Built.
 * Version:     1.4.0
 * Author:      lemonlolly
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

require_once plugin_dir_path( __FILE__ ) . 'chrome.php';

class TB_Content_Installer {

	public function __construct() {
		add_action( 'admin_menu', array( $this, 'menu' ) );
		add_action( 'admin_post_tb_install', array( $this, 'run' ) );
	}

	public function menu() {
		add_management_page(
			'Templeton Built', 'Templeton Built', 'manage_options',
			'tb-content', array( $this, 'screen' )
		);
	}

	public function screen() {
		$data = $this->data();
		echo '<div class="wrap"><h1>Templeton Built — Site Content</h1>';
		echo '<p>This will create or update <strong>' . count( $data ) . '</strong> pages and posts with their Divi layouts, '
		   . 'Rank Math titles and meta descriptions, and install the 301 redirect map.</p>';
		echo '<p>Existing items are matched by slug and <strong>overwritten</strong>. Safe to run more than once.</p>';
		echo '<form method="post" action="' . esc_url( admin_url( 'admin-post.php' ) ) . '">';
		wp_nonce_field( 'tb_install' );
		echo '<input type="hidden" name="action" value="tb_install">';
		submit_button( 'Install / update all content' );
		echo '</form></div>';
	}

	private function data() {
		$file = plugin_dir_path( __FILE__ ) . 'content.json';
		if ( ! file_exists( $file ) ) { return array(); }
		$json = json_decode( file_get_contents( $file ), true );
		return is_array( $json ) ? $json : array();
	}

	/** Find an existing page/post by slug regardless of status. */
	private function find( $slug, $type ) {
		$q = new WP_Query( array(
			'name'           => $slug,
			'post_type'      => $type,
			'post_status'    => array( 'publish', 'draft', 'pending', 'private', 'future' ),
			'posts_per_page' => 1,
			'fields'         => 'ids',
			'no_found_rows'  => true,
		) );
		return $q->have_posts() ? $q->posts[0] : 0;
	}

	public function run() {
		if ( ! current_user_can( 'manage_options' ) ) { wp_die( 'Not allowed.' ); }
		check_admin_referer( 'tb_install' );

		$data     = $this->data();
		$ids      = array();
		$created  = 0;
		$updated  = 0;

		// Pass 1 — parents before children so hierarchy resolves.
		foreach ( array( false, true ) as $children_pass ) {
			foreach ( $data as $slug => $item ) {
				$is_child = ! empty( $item['parent'] );
				if ( $is_child !== $children_pass ) { continue; }

				$type = ( 'post' === $item['type'] ) ? 'post' : 'page';
				$id   = $this->find( $slug, $type );

				$args = array(
					'post_title'   => $item['title'],
					'post_name'    => $slug,
					'post_content' => $item['content'],
					'post_status'  => 'publish',
					'post_type'    => $type,
				);
				if ( $is_child && isset( $ids[ $item['parent'] ] ) ) {
					$args['post_parent'] = $ids[ $item['parent'] ];
				}

				if ( $id ) {
					$args['ID'] = $id;
					wp_update_post( $args );
					$updated++;
				} else {
					$id = wp_insert_post( $args );
					$created++;
				}
				if ( is_wp_error( $id ) || ! $id ) { continue; }
				$ids[ $slug ] = $id;

				// Divi builder on, and clear its cached shortcode output.
				update_post_meta( $id, '_et_pb_use_builder', 'on' );
				update_post_meta( $id, '_et_pb_built_for_post_type', $type );
				delete_post_meta( $id, '_et_builder_module_features_cache' );

				// Rank Math meta.
				if ( ! empty( $item['seo_title'] ) ) {
					update_post_meta( $id, 'rank_math_title', wp_strip_all_tags( html_entity_decode( $item['seo_title'] ) ) );
				}
				if ( ! empty( $item['seo_desc'] ) ) {
					update_post_meta( $id, 'rank_math_description', wp_strip_all_tags( html_entity_decode( $item['seo_desc'] ) ) );
				}
				update_post_meta( $id, 'rank_math_robots', ! empty( $item['noindex'] ) ? array( 'noindex' ) : array( 'index' ) );
			}
		}

		// Static front page.
		if ( isset( $ids['home'] ) ) {
			update_option( 'show_on_front', 'page' );
			update_option( 'page_on_front', $ids['home'] );
		}
		// Blog index.
		if ( isset( $ids['journal'] ) ) {
			update_option( 'page_for_posts', $ids['journal'] );
		}

		$redirects = $this->redirects();

		// Clear Divi's static CSS/asset cache so new layouts render.
		if ( function_exists( 'et_core_clear_wp_cache' ) ) { et_core_clear_wp_cache(); }
		if ( class_exists( 'ET_Core_PageResource' ) && method_exists( 'ET_Core_PageResource', 'remove_static_resources' ) ) {
			ET_Core_PageResource::remove_static_resources( 'all', 'all' );
		}

		wp_safe_redirect( admin_url( 'tools.php?page=tb-content&done=1&c=' . $created . '&u=' . $updated . '&r=' . $redirects ) );
		exit;
	}

	/** Install the 301 map into Rank Math Redirections. */
	private function redirects() {
		if ( ! class_exists( '\RankMath\Redirections\DB' ) ) { return 0; }

		$map = array(
			'home-renovations-adelaide'            => '/renovations',
			'house-extensions-adelaide'            => '/extensions',
			'custom-new-homes'                     => '/custom-homes',
			'property-development-adelaide'        => '/custom-homes',
			'commercial-builders-adelaide'         => '/',
			'about-us'                             => '/about',
			'contact-us'                           => '/contact',
			'download-renovation-guide'            => '/cost-benchmark',
			'download-brochure'                    => '/architect-guide',
			'luxury-home-builder-adelaide'         => '/custom-homes',
			'house-extension-cost-adelaide'        => '/extensions',
			'home-extensions-adelaide-cost'        => '/extensions',
			'home-extension-and-renovation-costs'  => '/extensions',
			'home-extension-builders-adelaide'     => '/extensions',
			'home-renovation-builders-adelaide'    => '/renovations',
			'renovation-price-per-square-metre'    => '/renovations',
			'small-builder-near-me'                => '/about',
			'building-by-design'                   => '/custom-homes',
			'extension-design-and-build'           => '/extensions',
			'adelaide-restoration-centre'          => '/renovations',
			'benefits-of-boutique-builders-adelaide' => '/about',
		);

		$n = 0;
		foreach ( $map as $from => $to ) {
			try {
				$existing = \RankMath\Redirections\DB::match_redirections_source( $from );
				if ( ! empty( $existing ) ) { continue; }
				\RankMath\Redirections\DB::add( array(
					'sources'     => array( array( 'pattern' => $from, 'comparison' => 'exact' ) ),
					'url_to'      => $to,
					'header_code' => '301',
					'status'      => 'active',
				) );
				$n++;
			} catch ( \Exception $e ) { continue; }
		}
		return $n;
	}
}
new TB_Content_Installer();

add_action( 'admin_notices', function () {
	if ( empty( $_GET['done'] ) || empty( $_GET['page'] ) || 'tb-content' !== $_GET['page'] ) { return; }
	printf(
		'<div class="notice notice-success"><p><strong>Done.</strong> %d created, %d updated, %d redirects installed.</p></div>',
		(int) ( $_GET['c'] ?? 0 ), (int) ( $_GET['u'] ?? 0 ), (int) ( $_GET['r'] ?? 0 )
	);
} );
