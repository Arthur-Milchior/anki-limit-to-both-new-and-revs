from anki.sched import Scheduler as s1
from anki.schedv2 import Scheduler as s2
from anki.sched import *
from anki.schedv2 import *
from anki.lang import _
from .consts import *


currentSync = False

def counts(self, card=None):
        """The three numbers to show in anki deck's list/footer.
        Number of new cards, learning repetition, review card.

        If cards, then the tuple takes into account the card.
        sync -- whether it's called from sync, and the return must satisfies sync sanity check
        """
        counts = [self.newCount, self.lrnCount, self.revCount]
        if card:
            idx = self.countIdx(card)
            if idx == QUEUE_LRN:
                counts[1] += card.left // 1000
            else:
                counts[idx] += 1
        cur = self.col.decks.current()
        conf = self.col.decks.confForDid(cur['id'])
        if not currentSync:
            today = conf['perDay'] - cur['revToday'][1] - cur['newToday'][1]
            counts.append(today)
        return tuple(counts)
s1.counts = counts

def _deckNewLimitSingle(self, deck, sync=False):
        """Maximum number of new card to see today for deck deck, not considering parent limit.

        If deck is a dynamic deck, then reportLimit.
        Otherwise the number of card to see in this deck option, plus the number of card exceptionnaly added to this deck today.

        keyword arguments:
        deck -- a deck dictionnary
        sync -- whether it's called from sync, and the return must satisfies sync sanity check
        """
        if deck['dyn']:
            return self.reportLimit
        c = self.col.decks.confForDid(deck['id'])
        nbNewToSee = c['new']['perDay'] - deck['newToday'][1]
        if (not currentSync):
            nbCardToSee = c.get('perDay', 1000) - deck['revToday'][1] - deck['newToday'][1]
            limit = min(nbNewToSee, nbCardToSee)
        else:
            limit = nbNewToSee
        return max(0, limit)
s1._deckNewLimitSingle = _deckNewLimitSingle

def _deckRevLimitSingle(self, deck, sync=False):
        """Maximum number of card to review today in deck deck.

        self.reportLimit for dynamic deck. Otherwise the number of review according to deck option, plus the number of review added in custom study today.
        keyword arguments:
        deck -- a deck object
        sync -- whether it's called from sync, and the return must satisfies sync sanity check
        """
        if deck['dyn']:
            return self.reportLimit
        c = self.col.decks.confForDid(deck['id'])
        nbRevToSee = c['rev']['perDay'] - deck['revToday'][1]
        if (not currentSync):
            nbCardToSee = c.get('perDay', 1000) - deck['revToday'][1] - deck['newToday'][1]
            limit = min(nbRevToSee, nbCardToSee)
        else:
            limit = nbRevToSee
        return max(0, limit)
s1._deckRevLimitSingle = _deckRevLimitSingle

def counts(self, card=None, sync=False):
        """
        sync -- whether it's called from sync, and the return must satisfies sync sanity check
        """
        counts = [self.newCount, self.lrnCount, self.revCount]
        if card:
            idx = self.countIdx(card)
            counts[idx] += 1
        if (not currentSync):
            counts.append(counts[0] + counts[2]- deck['revToday'][1] - deck['newToday'][1] - deck['lrnToday'][1])
        return tuple(counts)
s2.counts = counts

def _deckNewLimitSingle(self, deck, sync=False):
        """Limit for deck without parent limits.
        sync -- whether it's called from sync, and the return must satisfies sync sanity check
        """
        if deck['dyn']:
            return self.dynReportLimit
        c = self.col.decks.confForDid(deck['id'])
        nbNewToSee = c['new']['perDay'] - deck['newToday'][1]
        if not currentSync:
            nbCardToSee = c.get('perDay', 1000) - deck['revToday'][1] - deck['newToday'][1]
            lim = min(nbNewToSee, nbCardToSee)
        else:
            lim = nbNewToSee
        return max(0, lim)

s2._deckNewLimitSingle = _deckNewLimitSingle

def _deckRevLimitSingle(self, deck, parentLimit=None, sync=False):
        """
        sync -- whether it's called from sync, and the return must satisfies sync sanity check
        """
        # invalid deck selected?
        if not deck:
            return 0

        if deck['dyn']:
            return self.dynReportLimit

        c = self.col.decks.confForDid(deck['id'])
        lim = max(0, c['rev']['perDay'] - deck['revToday'][1])
        if (not currentSync):
            nbCardToSee = c.get('perDay', 1000) - deck['revToday'][1] - deck['newToday'][1]
            lim = min(lim, nbCardToSee)

        if parentLimit is not None:
            return min(parentLimit, lim)
        elif '::' not in deck['name']:
            return lim
        else:
            for parent in self.col.decks.parents(deck['id']):
                # pass in dummy parentLimit so we don't do parent lookup again
                lim = min(lim, self._deckRevLimitSingle(parent, parentLimit=lim))
            return lim
s2._deckRevLimitSingle = _deckRevLimitSingle

from anki.sync import *
oldSanityCheck = Syncer.sanityCheck
def sanityCheck(self):
    currentSync = True
    oldSanityCheck(self)
    currentSync = False

Syncer.sanityCheck = sanityCheck

from PyQt5 import QtWidgets
from aqt.forms.dconf import *
oldsetupUi = Ui_Dialog.setupUi
def setupUi(self, Dialog):
    oldsetupUi(self, Dialog)
    self.totalPerDay = QtWidgets.QSpinBox(self.tab_5)
    self.totalPerDay.setObjectName("totalPerDay")
    self.gridLayout_5.addWidget(self.totalPerDay, 1, 1, 1, 1)
    self.label_16 = QtWidgets.QLabel(self.tab_5)
    self.label_16.setObjectName("label_16")
    self.gridLayout_5.addWidget(self.label_16, 1, 0, 1, 1)
    self.label_16.setText(_("total card/day"))
Ui_Dialog.setupUi = setupUi

from aqt.deckconf import *
oldLoadConf = DeckConf.loadConf
def loadConf(self):
    oldLoadConf(self)
    self.form.totalPerDay.setValue(self.conf.get('perDay', 1000))
DeckConf.loadConf = loadConf

oldSaveConf = DeckConf.saveConf
def saveConf(self):
    oldSaveConf(self)
    self.conf['perDay'] = self.form.totalPerDay.value()

DeckConf.saveConf = saveConf

from aqt.overview import *
def _table(self):
        counts = list(self.mw.col.sched.counts())
        finished = not sum(counts)
        if self.mw.col.schedVer() == 1:
            for n in range(len(counts)):
                if counts[n] >= 1000:
                    counts[n] = "1000+"
        but = self.mw.button
        if finished:
            return '<div style="white-space: pre-wrap;">%s</div>' % (
                self.mw.col.sched.finishedMsg())
        else:
            l = [
                (_("Learning"), counts[1], colLearn),
                (_("New"), counts[0], colNew),
                (_("To Review"), counts[2], colRev),
                (f"""{_("New")} + {_("To Review")}""", counts[3], colToday),
            ]
            return ('''
            <table width=400 cellpadding=5>
            <tr><td align=center valign=top>
            <table cellspacing=5>'''
                   +"\n              ".join([f'''<tr><td>{string}:</td><td><b><font color={col}>{count}</font></b></td></tr>'''
                               for string, count, col in l])
                   +f'''\
             </table>
           </td><td align=center>
           {but("study", _("Study Now"), id="study",extra=" autofocus")}</td></tr></table>''')
Overview._table = _table

from aqt.reviewer import *
def _remaining(self):
        if not self.mw.col.conf['dueCounts']:
            return ""
        if self.hadCardQueue:
            # if it's come from the undo queue, don't count it separately
            counts = list(self.mw.col.sched.counts())
        else:
            counts = list(self.mw.col.sched.counts(self.card))
        counts[0] = min(counts[0], counts[3])
        counts[2] = min(counts[2], counts[3])
        idx = self.mw.col.sched.countIdx(self.card)
        counts[idx] = "<u>%s</u>" % (counts[idx])
        return " + ".join([f'<font color="{col}">{count}</font>'
                    for col, count in [
                            (colNew, counts[0]),
                            (colLearn, counts[1]),
                            (colRev, counts[2]),]])

Reviewer._remaining = _remaining
