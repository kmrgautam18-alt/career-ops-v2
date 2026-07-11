from __future__ import annotations

QUESTION_BANK: dict[str, list[dict[str, str]]] = {
    "docker": [
        {
            "question": "Explain Docker architecture.",
            "difficulty": "Easy",
        },
        {
            "question": "Difference between Docker image and container?",
            "difficulty": "Easy",
        },
        {
            "question": "How does Docker networking work?",
            "difficulty": "Medium",
        },
    ],
    "kubernetes": [
        {
            "question": "What is Kubernetes?",
            "difficulty": "Easy",
        },
        {
            "question": "Explain Pods and Deployments.",
            "difficulty": "Medium",
        },
        {
            "question": "Difference between Deployment and StatefulSet.",
            "difficulty": "Hard",
        },
    ],
    "linux": [
        {
            "question": "Explain the Linux boot process.",
            "difficulty": "Medium",
        },
        {
            "question": "How do permissions work in Linux?",
            "difficulty": "Easy",
        },
    ],
    "terraform": [
        {
            "question": "What is Infrastructure as Code?",
            "difficulty": "Easy",
        },
        {
            "question": "Explain Terraform state file.",
            "difficulty": "Medium",
        },
    ],
    "ansible": [
        {
            "question": "What is an Ansible playbook?",
            "difficulty": "Easy",
        },
        {
            "question": "Difference between roles and playbooks.",
            "difficulty": "Medium",
        },
    ],
}