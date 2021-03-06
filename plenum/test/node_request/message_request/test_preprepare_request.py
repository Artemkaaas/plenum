from plenum.common.constants import PROPAGATE
from plenum.common.messages.node_messages import Prepare
from plenum.test.delayers import ppDelay, pDelay, ppgDelay, msg_rep_delay
from plenum.test.helper import send_reqs_batches_and_get_suff_replies
from plenum.test.node_catchup.helper import checkNodeDataForInequality, \
    waitNodeDataEquality
from plenum.test.node_request.message_request.helper import split_nodes
from plenum.test.spy_helpers import getAllReturnVals, get_count
from stp_core.loop.eventually import eventually


def count_requested_preprepare_resp(node):
    # Returns the number of times PRE-PREPARE was requested
    sr = node.master_replica
    return len(getAllReturnVals(sr, sr._request_pre_prepare_if_possible,
                                compare_val_to=True))


def count_requested_preprepare_req(node):
    # Returns the number of times an attempt was made to request PRE-PREPARE
    sr = node.master_replica
    return get_count(sr, sr._request_pre_prepare_if_possible)


def test_node_request_preprepare(looper, txnPoolNodeSet, client1,
                                    wallet1, client1Connected, teardown):
    """
    Node requests PRE-PREPARE only once after getting PREPAREs.
    """
    slow_node, other_nodes, primary_node, \
    other_primary_nodes = split_nodes(txnPoolNodeSet)
    # Drop PrePrepares and Prepares
    slow_node.nodeIbStasher.delay(ppDelay(300, 0))
    slow_node.nodeIbStasher.delay(pDelay(300, 0))

    send_reqs_batches_and_get_suff_replies(looper, wallet1, client1, 10, 5)
    slow_node.nodeIbStasher.drop_delayeds()
    slow_node.nodeIbStasher.resetDelays()

    old_count_req = count_requested_preprepare_req(slow_node)
    old_count_resp = count_requested_preprepare_resp(slow_node)

    def chk(increase=True):
        # Method is called
        assert count_requested_preprepare_req(slow_node) > old_count_req
        # Requesting Preprepare
        assert count_requested_preprepare_resp(slow_node) - old_count_resp == (1 if increase else 0)

    for pp in primary_node.master_replica.sentPrePrepares.values():
        for rep in [n.master_replica for n in other_primary_nodes]:
            prepare = Prepare(rep.instId,
                              pp.viewNo,
                              pp.ppSeqNo,
                              pp.digest,
                              pp.stateRootHash,
                              pp.txnRootHash
                              )
            rep.send(prepare)

        looper.run(eventually(chk, True, retryWait=1))

        old_count_resp = count_requested_preprepare_resp(slow_node)

        prepare = Prepare(rep.instId,
                          pp.viewNo,
                          pp.ppSeqNo,
                          pp.digest,
                          pp.stateRootHash,
                          pp.txnRootHash
                          )
        rep.send(prepare)

        looper.run(eventually(chk, False, retryWait=1))

        old_count_req = count_requested_preprepare_req(slow_node)

        old_count_resp = count_requested_preprepare_resp(slow_node)


def test_no_preprepare_requested(looper, txnPoolNodeSet, client1,
                                    wallet1, client1Connected, teardown):
    """
    Node missing Propagates hence request not finalised, hence stashes
    PRE-PREPARE but does not request PRE-PREPARE on receiving PREPARE
    """
    slow_node, other_nodes, _, _ = split_nodes(txnPoolNodeSet)
    slow_node.nodeIbStasher.delay(ppgDelay(20))
    slow_node.nodeIbStasher.delay(msg_rep_delay(20, [PROPAGATE, ]))

    old_count_resp = count_requested_preprepare_resp(slow_node)
    send_reqs_batches_and_get_suff_replies(looper, wallet1, client1, 4, 2)

    # The slow node is behind
    checkNodeDataForInequality(slow_node, *other_nodes)

    # PRE-PREPARE were not requested
    assert count_requested_preprepare_resp(slow_node) == old_count_resp

    slow_node.nodeIbStasher.reset_delays_and_process_delayeds()

    # The slow node has processed all requests
    waitNodeDataEquality(looper, slow_node, *other_nodes)

    # PRE-PREPARE were not requested
    assert count_requested_preprepare_resp(slow_node) == old_count_resp
