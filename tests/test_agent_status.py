from utils.agent_status import (
    create_job_status,
    update_job_status,
    update_agent_status,
    save_job_result,
    get_job_status
)


def test_agent_status_flow():
    job_id = "pytest-job"

    create_job_status(
        job_id
    )

    status = get_job_status(
        job_id
    )

    assert status is not None
    assert status["status"] == "waiting"

    assert (
        status["agents"]["researcher"]
        == "waiting"
    )

    update_job_status(
        job_id,
        "running"
    )

    update_agent_status(
        job_id,
        "researcher",
        "running"
    )

    status = get_job_status(
        job_id
    )

    assert status["status"] == "running"

    assert (
        status["agents"]["researcher"]
        == "running"
    )

    update_agent_status(
        job_id,
        "researcher",
        "completed"
    )

    save_job_result(
        job_id,
        {
            "final_answer": "Test tamamlandı."
        }
    )

    status = get_job_status(
        job_id
    )

    assert status["status"] == "completed"

    assert (
        status["agents"]["researcher"]
        == "completed"
    )

    assert (
        status["result"]["final_answer"]
        == "Test tamamlandı."
    )