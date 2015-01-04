#! /usr/bin/env python

import argparse
import ConfigParser
import os
import spotify as sp

def my_arg_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', '--username', required=True, help="Spotify Username")
	
	args = parser.parse_args()

	return args

def main():
    args = my_arg_parser()

    parent_dir = os.path.abspath(os.pardir)
    config_file = os.path.join(parent_dir, "config.ini")
    config = ConfigParser.ConfigParser()
    config.read(config_file)

    spotify_client_id = config.get('spotify', 'client_id')
    print "spotify_client_id"
    spotify_client_secret = config.get('spotify', 'client_secret')
    print "spotify_client_secret"
    spotify_token_url = config.get('spotify', 'token_url')
    print "spotify_token_url"
    token = sp.get_spotify_oauth_token(spotify_client_id, spotify_client_secret, spotify_token_url)
    print "get get_spotify_oauth_token"
    playlists = sp.get_user_playlists(token, args.username)
    print "get_user_playlists"
    track_urls = sp.get_playlist_track_urls(playlists, args.username)
    print "get_playlist_track_urls"
    track_data = sp.get_tracks(track_urls, token)
    print "get_tracks"
    parsed_data, json_data = sp.parse_track_data(track_data)
    print "parse_track_data"
    output_file = "track_data.json"
    output = os.path.abspath(os.path.realpath(output_file))

    sp.save_json_data(json_data, output)
    print "save_json_data"
    sorted_data = sp.sort_track_data(parsed_data)
    print "sort_track_data"
    sp.create_bar_chart(sorted_data)
    print "create_bar_chart"
if __name__ == "__main__":
    main()
