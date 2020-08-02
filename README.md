# limit number of cards by day (both new and review)
## Rationale
I believe that, if I reviewed many card in a deck, then I may not want
to also see new cards today in the same deck. This add-on is a first
and simple way to solve this problem; by adding a limit to the sum of
new cards and review cards seen by day.

In the reviewer, the numbers you'll see will take into account this
new limit; thus you may see a number of new cards decreasing while you
review a card; this is normal, it just means that you are reaching the
new limit.

In the overview window, you'll see the new limit as a separate number.

## Warning
Still experimental, not totally sure that it perfectly works with
subdecks.

This only works on PC, it does not change the number of cards to seen
according to Anki on Ios, ankiweb and ankidroid.

## Configuration
In the deck's option configuration, go to "general", and you'll find a
new option. You can here decide to limit the total number of cards.

By default this number is 1000, so hopefully, the default value won't
restrict you too much.

## Internal
This add-on modifies the following methods:
* anki.sched.Scheduler.counts
* anki.sched.Scheduler._deckNewLimitSingle
* anki.sched.Scheduler._deckRevLimitSingle
* anki.schedv2.Scheduler.counts
* anki.schedv2.Scheduler._deckNewLimitSingle
* anki.schedv2.Scheduler._deckRevLimitSingle
* anki.sync.Syncer.sanityCheck (calling the old version)
* aqt.form.dconf.Ui_Dialog.setupUi (calling the old version)
* aqt.deckconf.DeckConf.loadConf (calling the old version)
* aqt.deckconf.DeckConf.saveConf (calling the old version)
* aqt.overview.Overview._table
* aqt.reviewer.Reviewer._remaining = _remaining

## Version 2.0
None

## TODO
Create a way to decrease the number of new card without putting it to
0 when a lot of review cards have been seen

## Links, licence and credits

Key         |Value
------------|-------------------------------------------------------------------
Copyright   | Arthur Milchior <arthur@milchior.fr>
Based on    | Anki code by Damien Elmes <anki@ichi2.net>
License     | GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Source in   | https://github.com/Arthur-Milchior/anki-limit-to-both-new-and-revs
Addon number| [602339056](https://ankiweb.net/shared/info/602339056)
