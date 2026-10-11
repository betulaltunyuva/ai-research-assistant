from utils.agent_status import (
    create_job_status,
    update_job_status,
    update_agent_status,
    save_job_result,
    save_job_error,
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


def test_job_error_marks_running_agent_as_failed():
    job_id = "pytest-failed-job"

    create_job_status(
        job_id
    )

    update_agent_status(
        job_id,
        "researcher",
        "completed"
    )

    update_agent_status(
        job_id,
        "analyst",
        "running"
    )

    save_job_error(
        job_id,
        "Model yüklenemedi."
    )

    status = get_job_status(
        job_id
    )

    assert status["status"] == "failed"
    assert status["error"] == "Model yüklenemedi."

    assert (
        status["agents"]["researcher"]
        == "completed"
    )

    assert (
        status["agents"]["analyst"]
        == "failed"
    )

    assert (
        status["agents"]["writer"]
        == "waiting"
    )
