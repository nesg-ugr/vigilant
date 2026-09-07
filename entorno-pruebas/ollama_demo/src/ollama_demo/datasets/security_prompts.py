"""Dataset of security and network trace prompts for testing LLM capabilities."""

SYS_CYBERSECURITY_ANALYST = (
    "You are an expert Cybersecurity Operations Center (SOC) analyst. "
    "Analyze network artifacts, logs, and traces. Be concise, precise, "
    "and highlight potential attack vectors or anomalies."
)

PROMPT_PCAP_ANALYSIS = """
Analyze the following TCP dump summary and identify potential security threats:

192.168.1.50:49152 -> 10.0.0.5:80 TCP SYN
10.0.0.5:80 -> 192.168.1.50:49152 TCP SYN-ACK
192.168.1.50:49152 -> 10.0.0.5:80 TCP ACK
192.168.1.50:49152 -> 10.0.0.5:80 HTTP POST /login.php ('OR 1=1 --)
10.0.0.5:80 -> 192.168.1.50:49152 HTTP 200 OK (Content-Length: 4520)

What attack vector is present here, and what immediate remediation steps should be taken?
"""

PROMPT_LOG_EXFILTRATION = """
Review this firewalled outbound DNS query log:

2026-09-03T10:15:01Z QNAME: a3f89b1c.exfil.attacker-domain.com TYPE: TXT
2026-09-03T10:15:02Z QNAME: d9e02f41.exfil.attacker-domain.com TYPE: TXT
2026-09-03T10:15:03Z QNAME: c1b3a4f9.exfil.attacker-domain.com TYPE: TXT

Explain what technique is being executed and how DNS tunneling operates.
"""