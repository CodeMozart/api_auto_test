# -*- coding: utf-8 -*-

import logging
import json
from libs.crawle.download import Downloader


class RiotLolMatch:
    def __init__(self, cache=None):
        self.cache = cache

    def get_match_detail(self, tournament_id, match_id, json_decode=True):
        url = 'http://api.lolesports.com/api/v2/highlanderMatchDetails?tournamentId=%s&matchId=%s' \
              % (tournament_id, match_id)
        logging.info('match detail: %s' % url)
        d = Downloader(cache=self.cache)
        match_detail = d(url)
        if not match_detail:
            return False

        if json_decode:
            match_detail = json.loads(match_detail)
        return match_detail

    def get_schedule_items(self, cp_event_id, json_decode=True):
        url = 'http://api.lolesports.com/api/v1/scheduleItems?leagueId=%s' % cp_event_id
        d = Downloader(self.cache)
        league_schedule = d(url)
        if not league_schedule:
            return False

        if json_decode:
            league_schedule = json.loads(league_schedule)
        return league_schedule

    def get_stats(self, game_realm, game_id, game_hash, json_decode=True):
        url = 'https://acs.leagueoflegends.com/v1/stats/game/%s/%s?gameHash=%s' % (game_realm, game_id, game_hash)
        d = Downloader(self.cache)
        stats = d(url)
        if not stats:
            return False

        if json_decode:
            stats = json.loads(stats)
        return stats

    def get_timeline(self, game_realm, game_id, game_hash, json_decode=True):
        url = 'https://acs.leagueoflegends.com/v1/stats/game/%s/%s/timeline?gameHash=%s' \
              % (game_realm, game_id, game_hash)
        d = Downloader(self.cache)
        timelime = d(url)
        if not timelime:
            return False

        if json_decode:
            timelime = json.loads(timelime)
        return timelime
