from typing import TypeVar, NamedTuple

from plenum.common.constants import *
from plenum.common.messages.fields import *
from plenum.common.messages.message_base import MessageBase
from plenum.common.types import f
from plenum.common.messages.client_request import ClientMessageValidator


class Nomination(MessageBase):
    typename = NOMINATE

    schema = (
        (f.NAME.nm, NonEmptyStringField()),
        (f.INST_ID.nm, NonNegativeNumberField()),
        (f.VIEW_NO.nm, NonNegativeNumberField()),
        (f.ORD_SEQ_NO.nm, NonNegativeNumberField()),
    )


class Batch(MessageBase):
    typename = BATCH

    schema = (
        (f.MSGS.nm, IterableField(SerializedValueField())),
        (f.SIG.nm, SignatureField()),
    )


class Reelection(MessageBase):
    typename = REELECTION

    schema = (
        (f.INST_ID.nm, NonNegativeNumberField()),
        (f.ROUND.nm, NonNegativeNumberField()),
        (f.TIE_AMONG.nm, IterableField(TieAmongField())),
        (f.VIEW_NO.nm, NonNegativeNumberField()),
    )


class Primary(MessageBase):
    typename = PRIMARY

    schema = (
        (f.NAME.nm, NonEmptyStringField()),
        (f.INST_ID.nm, NonNegativeNumberField()),
        (f.VIEW_NO.nm, NonNegativeNumberField()),
        (f.ORD_SEQ_NO.nm, NonNegativeNumberField()),
    )


# TODO implement actual rules
class BlacklistMsg(MessageBase):
    typename = BLACKLIST
    schema = (
        (f.SUSP_CODE.nm, AnyValueField()),
        (f.NODE_NAME.nm, AnyValueField()),
    )


# TODO implement actual rules
class RequestAck(MessageBase):
    typename = REQACK
    schema = (
        (f.IDENTIFIER.nm, AnyValueField()),
        (f.REQ_ID.nm, AnyValueField())
    )


# TODO implement actual rules
class RequestNack(MessageBase):
    typename = REQNACK
    schema = (
        (f.IDENTIFIER.nm, AnyValueField()),
        (f.REQ_ID.nm, AnyValueField()),
        (f.REASON.nm, AnyValueField()),
    )


# TODO implement actual rules
class Reject(MessageBase):
    typename = REJECT
    schema = (
        (f.IDENTIFIER.nm, AnyValueField()),
        (f.REQ_ID.nm, AnyValueField()),
        (f.REASON.nm, AnyValueField()),
    )


# TODO implement actual rules
class PoolLedgerTxns(MessageBase):
    typename = POOL_LEDGER_TXNS
    schema = (
        (f.TXN.nm, AnyValueField()),
    )


class Ordered(MessageBase):
    typename = ORDERED
    schema = (
        (f.INST_ID.nm, NonNegativeNumberField()),
        (f.VIEW_NO.nm, NonNegativeNumberField()),
        (f.REQ_IDR.nm, IterableField(RequestIdentifierField())),
        (f.PP_SEQ_NO.nm, NonNegativeNumberField()),
        (f.PP_TIME.nm, TimestampField()),
        (f.LEDGER_ID.nm, LedgerIdField()),
        (f.STATE_ROOT.nm, MerkleRootField(nullable=True)),
        (f.TXN_ROOT.nm, MerkleRootField(nullable=True)),
    )


class Propagate(MessageBase):
    typename = PROPAGATE
    schema = (
        (f.REQUEST.nm, ClientMessageValidator(operation_schema_is_strict=True)),
        (f.SENDER_CLIENT.nm, NonEmptyStringField(nullable=True)),
    )


class PrePrepare(MessageBase):
    typename = PREPREPARE
    schema = (
        (f.INST_ID.nm, NonNegativeNumberField()),
        (f.VIEW_NO.nm, NonNegativeNumberField()),
        (f.PP_SEQ_NO.nm, NonNegativeNumberField()),
        (f.PP_TIME.nm, TimestampField()),
        (f.REQ_IDR.nm, IterableField(RequestIdentifierField())),
        (f.DISCARDED.nm, NonNegativeNumberField()),
        (f.DIGEST.nm, NonEmptyStringField()),
        (f.LEDGER_ID.nm, LedgerIdField()),
        (f.STATE_ROOT.nm, MerkleRootField(nullable=True)),
        (f.TXN_ROOT.nm, MerkleRootField(nullable=True)),
    )


class Prepare(MessageBase):
    typename = PREPARE
    schema = (
        (f.INST_ID.nm, NonNegativeNumberField()),
        (f.VIEW_NO.nm, NonNegativeNumberField()),
        (f.PP_SEQ_NO.nm, NonNegativeNumberField()),
        (f.DIGEST.nm, NonEmptyStringField()),
        (f.STATE_ROOT.nm, MerkleRootField(nullable=True)),
        (f.TXN_ROOT.nm, MerkleRootField(nullable=True)),
    )


class Commit(MessageBase):
    typename = COMMIT
    schema = (
        (f.INST_ID.nm, NonNegativeNumberField()),
        (f.VIEW_NO.nm, NonNegativeNumberField()),
        (f.PP_SEQ_NO.nm, NonNegativeNumberField()),
    )


class Checkpoint(MessageBase):
    typename = CHECKPOINT
    schema = (
        (f.INST_ID.nm, NonNegativeNumberField()),
        (f.VIEW_NO.nm, NonNegativeNumberField()),
        (f.SEQ_NO_START.nm, NonNegativeNumberField()),
        (f.SEQ_NO_END.nm, NonNegativeNumberField()),
        (f.DIGEST.nm, NonEmptyStringField()),
    )


class ThreePCState(MessageBase):
    typename = THREE_PC_STATE
    schema = (
        (f.INST_ID.nm, NonNegativeNumberField()),
        (f.MSGS.nm, IterableField(ClientMessageValidator(operation_schema_is_strict=True))),
    )


# TODO implement actual rules
class CheckpointState(MessageBase):
    typename = CHECKPOINT_STATE
    schema = (
        (f.SEQ_NO.nm, AnyValueField()),
        (f.DIGESTS.nm, AnyValueField()),
        (f.DIGEST.nm, AnyValueField()),
        (f.RECEIVED_DIGESTS.nm, AnyValueField()),
        (f.IS_STABLE.nm, AnyValueField())
    )


# TODO implement actual rules
class Reply(MessageBase):
    typename = REPLY
    schema = (
        (f.RESULT.nm, AnyValueField()),
    )


class InstanceChange(MessageBase):
    typename = INSTANCE_CHANGE
    schema = (
        (f.VIEW_NO.nm, NonNegativeNumberField()),
        (f.REASON.nm, NonNegativeNumberField())
    )


class LedgerStatus(MessageBase):
    """
    Purpose: spread status of ledger copy on a specific node.
    When node receives this message and see that it has different
    status of ledger it should reply with LedgerStatus that contains its
    status
    """
    typename = LEDGER_STATUS
    schema = (
        (f.LEDGER_ID.nm, LedgerIdField()),
        (f.TXN_SEQ_NO.nm, NonNegativeNumberField()),
        (f.VIEW_NO.nm, NonNegativeNumberField(nullable=True)),
        (f.PP_SEQ_NO.nm, NonNegativeNumberField(nullable=True)),
        (f.MERKLE_ROOT.nm, MerkleRootField()),
    )


class ConsistencyProof(MessageBase):
    typename = CONSISTENCY_PROOF
    schema = (
        (f.LEDGER_ID.nm, LedgerIdField()),
        (f.SEQ_NO_START.nm, NonNegativeNumberField()),
        (f.SEQ_NO_END.nm, NonNegativeNumberField()),
        (f.VIEW_NO.nm, NonNegativeNumberField()),
        (f.PP_SEQ_NO.nm, NonNegativeNumberField()),
        (f.OLD_MERKLE_ROOT.nm, MerkleRootField()),
        (f.NEW_MERKLE_ROOT.nm, MerkleRootField()),
        (f.HASHES.nm, IterableField(NonEmptyStringField())),
    )


class CatchupReq(MessageBase):
    typename = CATCHUP_REQ
    schema = (
        (f.LEDGER_ID.nm, LedgerIdField()),
        (f.SEQ_NO_START.nm, NonNegativeNumberField()),
        (f.SEQ_NO_END.nm, NonNegativeNumberField()),
        (f.CATCHUP_TILL.nm, NonNegativeNumberField()),
    )


class CatchupRep(MessageBase):
    typename = CATCHUP_REP
    schema = (
        (f.LEDGER_ID.nm, LedgerIdField()),
        # TODO: turn on validation, the cause is INDY-388
        # (f.TXNS.nm, MapField(key_field=StringifiedNonNegativeNumberField(),
        #                      value_field=ClientMessageValidator(operation_schema_is_strict=False))),
        (f.TXNS.nm, AnyValueField()),
        (f.CONS_PROOF.nm, IterableField(Base58Field(byte_lengths=(32,)))),
    )
    

class ViewChangeDone(MessageBase):
    """
    Node sends this kind of message when view change steps done and it is
    ready to switch to the new primary.
    In contrast to 'Primary' message this one does not imply election.
    """
    typename = VIEW_CHANGE_DONE

    schema = (
        # name is nullable because this message can be sent when
        # there were no view changes and instance has no primary yet
        (f.VIEW_NO.nm, NonNegativeNumberField()),
        (f.NAME.nm, NonEmptyStringField(nullable=True)),
        (f.LEDGER_INFO.nm, IterableField(LedgerInfoField()))
    )


"""
The choice to do a generic 'request message' feature instead of a specific
one was debated. It has some pros and some cons. We wrote up the analysis in
http://bit.ly/2uxf6Se. This decision can and should be revisited if we feel a
lot of ongoing dissonance about it. Lovesh, Alex, and Daniel, July 2017
"""
class MessageReq(MessageBase):
    """
    Purpose: ask node for any message
    """
    allowed_types = {LEDGER_STATUS, CONSISTENCY_PROOF, PREPREPARE,
                     PROPAGATE}
    typename = MESSAGE_REQUEST
    schema = (
        (f.MSG_TYPE.nm, ChooseField(values=allowed_types)),
        (f.PARAMS.nm, AnyMapField())
    )


class MessageRep(MessageBase):
    """
    Purpose: respond to a node for any requested message
    """
    # TODO: support a setter for `msg` to create an instance of a type according to `msg_type`
    typename = MESSAGE_RESPONSE
    schema = (
        (f.MSG_TYPE.nm, ChooseField(values=MessageReq.allowed_types)),
        (f.PARAMS.nm, AnyMapField()),
        (f.MSG.nm, AnyField())
    )


ThreePhaseType = (PrePrepare, Prepare, Commit)
ThreePhaseMsg = TypeVar("3PhaseMsg", *ThreePhaseType)


ElectionType = (Nomination, Primary, Reelection)
ElectionMsg = TypeVar("ElectionMsg", *ElectionType)

ThreePhaseKey = NamedTuple("ThreePhaseKey", [
                        f.VIEW_NO,
                        f.PP_SEQ_NO
                    ])
