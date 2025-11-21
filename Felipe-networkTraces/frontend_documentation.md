# VIGILANT Web UI Specification (Frontend - Next.js, React + Tailwind)

## 1. Overview

VIGILANT is a cybersecurity analysis console designed to host **multiple investigation use cases**.  
The initial use case is the analysis of **network traces from PCAP files**, but the Web UI must be structured so that additional cybersecurity use cases can be added later (for example, endpoint logs, cloud audit logs, email telemetry, etc.).

The Web UI is a single-page-style application built with:

- **Next.js (App Router)**
- **React**
- **Tailwind CSS**

The UI provides, across all use cases:

- A common layout and navigation structure under the VIGILANT brand.
- Basic configuration and connectivity to the VIGILANT backend.
- Per-use-case sections with their own pages and flows.

For the **initial network traces use case**, the UI provides:

- Management of PCAP files.
- Creation and handling of **investigations** tied to PCAPs.
- A **chat-style interface** for Phase 1 technical Q&A (analyst + tools + LLM).
- Controls for Phase 2 intelligence report generation.
- Viewing and downloading of **PDF reports**.
- Global **history and search**, including **RAG-based search** across past reports.

The UI communicates with the VIGILANT backend over HTTP/JSON using an API key.

Throughout the UI, the project name **VIGILANT** should be visible in the main layout (e.g., sidebar header or top bar).

---

## 2. Backend Integration

### 2.1 Connection Configuration

The Web UI interacts with the VIGILANT backend via a configurable base URL and API key.

Configuration requirements:

- On first load, if no configuration is stored, the app displays a **Connection Settings** view or modal to collect:
  - **Backend URL** (e.g., `http://localhost:8000`).
  - **API key**.
- These values are persisted in `localStorage` (or an equivalent browser storage) and reused on subsequent loads.
- There is a dedicated **Settings** page where these values can be reviewed and changed.

All API requests include:

- `Authorization: Bearer <API_KEY>`
- `Content-Type: application/json` for JSON endpoints.
- For file uploads, `multipart/form-data` is used, with the same `Authorization` header.

### 2.2 Health Check

The UI uses a health endpoint to verify connectivity:

- `GET /health`
- Expected response body (example): 

```json
{ "status": "ok", "version": "..." }
```

`status` is the key field; other fields may be present.

A "Test connection" button in the Settings view calls this endpoint and reports success or any connection error to the user.

---

## 3. Global Layout and Navigation

### 3.1 Application Shell

VIGILANT Web UI uses a standard application shell with the following main elements:

- **Top bar**:
  - Displays the VIGILANT name and logo/wordmark (e.g., `VIGILANT` on the left).
  - Optionally displays current connection status:
    - A small colored indicator (green/red).
    - Summary text such as "Connected to `<backend URL>`".

- **Left sidebar**:
  - Navigation entries grouped logically:
    - **Home / Dashboard**
    - **Use Cases**
      - **Network Traces (PCAP)** - the initial use case.
      - (Placeholder for future use cases, e.g., "Endpoint Logs", "Cloud Audit Logs".)
    - **Search**
    - **Settings**

- **Main content area**:
  - Displays the currently selected page for the chosen route.

Tailwind is used for layout, spacing, typography, and components.

---

## 4. Use Case Framework

VIGILANT is intended to support multiple cybersecurity use cases. The Web UI must present these as **modules** or **sections** under a common shell.

### 4.1 Use Case Concept

A **Use Case** in the UI is a logical grouping of functionality:

- Example use case: **Network Traces (PCAP)**.
- Future use cases might be:
  - Endpoint telemetry analysis.
  - Cloud audit log analysis.
  - Email security investigations.

Each use case:

- Has a **name**, **description**, and **icon**.
- Has a **route prefix** or section in the navigation.
- Contains its own pages and flows.

The initial implementation must:

- Show **Network Traces (PCAP)** as the first and only fully implemented use case.
- Structure the navigation so new use cases can be added later without disrupting the layout.

### 4.2 Global Dashboard

**Route:** `/` (root)

The dashboard may:

- Briefly introduce VIGILANT.
- Show **cards** for each available use case:
  - Network Traces (PCAP) - with a short description and "Open" button.
  - Placeholder cards for future use cases (visually present but disabled or "Coming soon").

Clicking a use case card navigates to the primary page of that use case (for Network Traces, this is `/pcaps`).

---

## 5. Settings Page

**Route:** `/settings`

### 5.1 Purpose

The Settings page allows configuration of the VIGILANT backend connection and displays current settings.

### 5.2 Fields

- **Backend URL** (text input)
- **API key** (password input, with an option to show/hide characters)

### 5.3 Actions

- **Test Connection**:
  - Calls `GET /health` on the configured backend URL.
  - Displays:
    - Success message (e.g., "Connected to VIGILANT backend - version X.Y").
    - Or error message if unreachable or if `status` is not `"ok"`.

- **Save**:
  - Stores values in `localStorage`.
  - Updates any in-memory configuration used by the API client.

---

## 6. Network Traces Use Case (Initial Module)

The initial implemented use case in VIGILANT is **Network Traces (PCAP)**. All the sections below describe the UI for this use case.

Top-level entry in the sidebar should be labeled:

- "Network Analysis" with a sublabel/description "PCAP traces".

The routes in this section are:

- `/pcaps`
- `/pcaps/[pcap_id]`
- `/investigations`
- `/investigations/[investigation_id]`
- `/search` (cross-investigation RAG search, for all use cases; initially only PCAP-related data exists)

---

### 6.1. PCAP Management

#### 6.1.1 PCAP List

**Route:** `/pcaps`

This page lists all PCAPs known to the VIGILANT backend.

##### Layout

- Header bar:
  - Title: `PCAPs - VIGILANT`
  - Subtitle or badge indicating "Network Traces use case".
  - Primary action: `Upload PCAP` button.

- Content:
  - Table of PCAPs with columns:
    - **Filename** (`original_filename`)
    - **Uploaded at** (`uploaded_at`, formatted)
    - **Size** (`file_size_bytes`, converted to KB/MB/GB)
    - **Status** (`uploaded`, `parsed`, `parse_failed`)
    - **Investigations** (number of investigations for this PCAP, if provided)
    - **Action**: `Open` button to view PCAP details.

##### Backend Endpoint

- `GET /pcaps`

Expected response shape (example):

```json
[
  {
    "pcap_id": "uuid-1",
    "original_filename": "capture1.pcap",
    "uploaded_at": "2025-11-20T10:00:00Z",
    "file_size_bytes": 12345678,
    "status": "parsed",
    "investigations_count": 2
  }
]
```

#### 6.1.2 Upload PCAP

Clicking "Upload PCAP" opens a modal dialog:

- Fields:
  - File input (PCAP file).

- Actions:
  - "Upload" button.
  - "Cancel" button.

When "Upload" is clicked:

- UI performs `POST /pcaps/upload` with `multipart/form-data`:
  - Field name: `file`.

Successful response example:

```json
{
  "pcap_id": "uuid-1",
  "status": "uploaded"
}
```

After a successful upload:

- The modal closes.
- The PCAP list is refreshed (re-call `GET /pcaps`).

---

### 6.2. PCAP Detail and Investigations List

**Route:** `/pcaps/[pcap_id]`

#### 6.2.1 Purpose

This page presents metadata about a specific PCAP and a list of investigations associated with it.

#### 6.2.2 Layout

- **PCAP summary card**:
  - Filename
  - Uploaded at
  - Size
  - Status
  - Optional notes (if provided later)

- **Actions**:
  - `Start new investigation` button.

- **Investigations list**:
  - Table with columns:
    - Investigation title
    - Started at
    - Status (`active`, `completed`, etc.)
    - Report status (`has_report` flag)
    - Action: `Open` (navigates to investigation workspace).

#### 6.2.3 Backend Endpoints

- `GET /pcaps/{pcap_id}`

Example response:

```json
{
  "pcap_id": "uuid-1",
  "original_filename": "capture1.pcap",
  "uploaded_at": "2025-11-20T10:00:00Z",
  "file_size_bytes": 12345678,
  "status": "parsed"
}
```

- `GET /investigations?pcap_id={pcap_id}`

Example response:

```json
[
  {
    "investigation_id": "inv-1",
    "pcap_id": "uuid-1",
    "title": "SSH anomalies in capture1",
    "started_at": "2025-11-20T10:30:00Z",
    "status": "active",
    "has_report": true
  }
]
```

- `POST /pcaps/{pcap_id}/investigations`

Example request body:

```json
{
  "title": "Optional investigation title"
}
```

Example response:

```json
{
  "investigation_id": "inv-1",
  "status": "active"
}
```

After starting a new investigation, the UI may directly navigate to `/investigations/[investigation_id]`.

---

### 6.3. Investigation Workspace (Phase 1 + Phase 2)

**Route:** `/investigations/[investigation_id]`

This is the central interactive workspace for a VIGILANT investigation in the Network Traces use case.

#### 6.3.1 Layout Overview

Recommended layout:

- **Top or left: Investigation context**
  - VIGILANT branding visible (e.g., "VIGILANT - Network Traces").
  - Investigation title (editable).
  - Investigation metadata:
    - `status` (active/completed)
    - `started_at`, `completed_at`
  - PCAP summary (filename, link to PCAP detail).

- **Center: Chat-style transcript**
  - Conversation view with messages in chronological order.
  - New message input at the bottom.

- **Right-side panel or tab: Report**
  - Shows intelligence report when available.
  - Provides a button to generate or regenerate the report.
  - Offers PDF download.

#### 6.3.2 Message Model

Messages are retrieved and displayed as a chat-style transcript.

Backend response example for messages (from `GET /investigations/{id}/messages`):

```json
#### 6.3.2 Message Model

Messages are retrieved and displayed as a chat-style transcript.

Backend response example for messages (from `GET /investigations/{id}/messages`):

```json
[
  {
    "id": "msg-1",
    "investigation_id": "inv-1",
    "role": "analyst",
    "type": "question",
    "content": {
      "text": "How many public IPs are in this trace?",
      "data": null,
      "format": "markdown"
    },
    "tool_name": null,
    "created_at": "2025-11-20T10:35:00Z"
  },
  {
    "id": "msg-2",
    "investigation_id": "inv-1",
    "role": "tool",
    "type": "tool_result",
    "content": {
      "text": null,
      "data": {
        "total_unique_ips": 42,
        "public_ips": ["198.51.100.1"],
        "private_ips": ["10.0.0.1"]
      },
      "format": "json"
    },
    "tool_name": "layer3_summary",
    "created_at": "2025-11-20T10:35:05Z"
  },
  {
    "id": "msg-3",
    "investigation_id": "inv-1",
    "role": "assistant",
    "type": "answer",
    "content": {
      "text": "There are 42 unique IPs and 1 public IP: 198.51.100.1.",
      "data": null,
      "format": "markdown"
    },
    "tool_name": null,
    "created_at": "2025-11-20T10:35:07Z"
  }
]
```

Main chat UI rendering:

- For `role = "analyst"`:
  - Render `content.text` as a "user" chat bubble.
- For `role = "assistant"`:
  - Render `content.text` as an "assistant" bubble, with markdown support.
- Messages with a `role = "tool"` are **not shown** in the main chat transcript.

Tool messages are still part of the message model and are returned by the API for audit/debug purposes. A future "debug" or "details" panel could optionally render them, for example as cards showing:

- Tool name (e.g., `layer3_summary`).
- For `content.format = "json"`, a collapsible JSON viewer or `<pre>` view.
- For `content.format = "markdown"`, rendered markdown.

In the MVP, the primary chat view only displays analyst and assistant messages.

#### 6.3.3 Loading Existing Messages

On entering `/investigations/[investigation_id]`:

- The UI calls `GET /investigations/{id}/messages`.
- The backend returns the full transcript for that investigation, including messages with `role = "analyst"`, `role = "assistant"`, and `role = "tool"`.
- The UI **filters out tool messages** and only renders:
  - `role = "analyst"` (analyst questions)
  - `role = "assistant"` (LLM answers)
- Messages are sorted by `created_at` in ascending order.
- The chat view is populated from this filtered list.

Tool messages remain available in the API response and database for audit/debug purposes but are not shown in the main chat transcript in the VIGILANT Web UI.


#### 6.3.4 Sending Analyst Questions (Phase 1)

At the bottom of the workspace:

- A text area for analyst questions.
- A "Send" button.

When the analyst submits a question, it is immediately shown in the chat transcript as a new analyst message, and the following actions take place:

1. The UI sends:

   `POST /investigations/{id}/messages`

   With body:

   ```json
   {
     "role": "analyst",
     "content": {
       "text": "<question text>"
     }
   }
   ```

2. The backend:
   - Stores the analyst message in `investigation_messages`.
   - Runs the LangGraph workflow:
    - Calls OSI-layer tools as needed.
    - Stores their outputs as `role = "tool"` messages (for audit and debugging; the UI will not show them in the main chat transcript).
    - Generates the assistant answer and stores it as a `role = "assistant"` message.
   - Returns only the assistant answer created in this run.

3. The backend returns the assistant answer in a field such as `assistant_answer`, which has the same shape as a message object from `GET /investigations/{id}/messages`:

```json
{
  "assistant_answer": {
    "id": "msg-103",
    "role": "assistant",
    "type": "answer",
    "content": {
      "text": "There are 5 public IPs...",
      "data": null,
      "format": "markdown"
    },
    "tool_name": null,
    "created_at": "..."
  }
}
```

4. The UI appends this `assistant_answer` to the transcript and scrolls to the bottom.

While waiting for the response, the input should be disabled and a spinner shown.

VOY POR AQUI

#### 6.3.5 Intelligence Report Panel (Phase 2)

The right-side panel or a tab shows the intelligence report.

##### 6.3.5.1 Viewing Reports

- `GET /investigations/{id}/report`

Example response:

```json
{
  "report_id": "rep-999",
  "investigation_id": "inv-1",
  "title": "SSH Brute Force Activity in capture1.pcap",
  "created_at": "2025-11-20T11:00:00Z",
  "summary_text": "## Executive Summary\n...",
  "metadata": {
    "severity": "critical",
    "protocols": ["SSH"],
    "tags": ["brute_force"]
  },
  "pdf_available": true
}
```

UI behavior:

- If a report exists:
  - Display `title`.
  - Render `summary_text` as markdown in a scrollable area.
  - Show severity, protocols, tags using colored badges or chips.
  - Provide a "Download PDF" button that opens `/investigations/{id}/report.pdf` in a new tab or triggers a download.

- If no report exists:
  - Display a message: "No intelligence report has been generated yet."
  - Provide a "Generate intelligence report" button.

##### 6.3.5.2 Generating Reports

- Button: `Generate intelligence report`.
- Action:

  `POST /investigations/{id}/generate_report`

- The backend runs a Phase 2 workflow to:
  - Read the transcript.
  - Generate a markdown report.
  - Extract metadata (severity, protocols, tags).
  - Render and store the PDF.

- The response returns report metadata in the same shape as `GET /investigations/{id}/report`.

UI behavior:

- While the request is ongoing, show a loading indicator.
- After success, call `GET /investigations/{id}/report` to refresh the panel.

---

### 6.4 Investigations & Reports Overview

**Route:** `/reports` or `/investigations`

#### 6.4.1 Purpose

Provides a global view of all investigations and their reports in VIGILANT, with filtering capabilities.  
Initially, all investigations are from the Network Traces use case, but the backend may later support investigations from additional use cases.

#### 6.4.2 Layout

- Filters at the top:
  - Date range: `From` and `To` (applied to report `created_at` or investigation `started_at`).
  - Severity dropdown:
    - All, Informational, Low, Medium, High, Critical.
  - Protocol tags:
    - Multi-select (e.g., RDP, SSH, HTTP, DNS, etc.).
  - Optional use case filter:
    - For future extension (e.g., `use_case = "network_traces"`).

- Table of investigations:
  - Columns:
    - Investigation title
    - PCAP filename (or appropriate dataset label for other use cases)
    - Severity (from report metadata)
    - Protocols (tags from metadata)
    - Report date
    - Status (from `investigations.status`)
    - Action: "Open" → `/investigations/[id]`.

#### 6.4.3 Backend Endpoint

- `GET /investigations` with optional query parameters:
  - `pcap_id`
  - `status`
  - `severity`
  - `protocol`
  - `from`
  - `to`
  - (Potential future filter) `use_case`

Example response:

```json
[
  {
    "investigation_id": "inv-1",
    "pcap_id": "uuid-1",
    "title": "SSH anomalies in capture1",
    "started_at": "2025-11-20T10:30:00Z",
    "status": "completed",
    "report": {
      "report_id": "rep-999",
      "created_at": "2025-11-20T11:00:00Z",
      "metadata": {
        "severity": "critical",
        "protocols": ["SSH"],
        "tags": ["brute_force"]
      }
    },
    "pcap": {
      "original_filename": "capture1.pcap"
    }
  }
]
```

The UI uses this data for the overview table and links back to each investigation's workspace.

---

### 6.5 RAG-Based Search Page

**Route:** `/search`

#### 6.5.1 Purpose

Allows analysts to perform semantic search over past VIGILANT investigation reports using the RAG results from the backend.  
This page is global across use cases, but in the MVP, only Network Traces (PCAP) reports will be available.

#### 6.5.2 Layout

- Search bar:
  - Placeholder: "Search past VIGILANT investigations (e.g., ‘SSH brute force on RDP jump box')…".
  - "Search" button.

- Optional result summary:
  - Text summary from LLM (e.g., "VIGILANT found 3 similar investigations…").

- Filters (optional, to align with backend capabilities):
  - Severity.
  - Protocol.
  - Date range.
  - (Future) Use case.

- Results list:
  - Cards or rows showing:
    - Report title.
    - Short snippet (from the match).
    - Severity and protocols (badges).
    - Score (if desired).
    - "Open investigation" button linking to `/investigations/[investigation_id]`.

#### 6.5.3 Backend Endpoint

- `POST /rag/reports/query`

Example request:

```json
{
  "query": "SSH brute force against RDP jump box",
  "top_k": 5
}
```

Example response:

```json
{
  "answer": "VIGILANT has identified 3 similar past investigations involving SSH brute force attempts to internal servers.",
  "matches": [
    {
      "report_id": "rep-999",
      "investigation_id": "inv-1",
      "title": "SSH brute force in DMZ",
      "snippet": "In this investigation, repeated failed SSH attempts...",
      "score": 0.12,
      "metadata": {
        "severity": "critical",
        "protocols": ["SSH"],
        "tags": ["brute_force"]
      }
    }
  ]
}
```

The `answer` text can be displayed above the results list as an LLM-generated summary.

---

## 7. Frontend Architecture and Components (Next.js + Tailwind)

### 7.1 Project Structure

The Web UI is implemented with Next.js (App Router) and a `src/` directory enabled.

Suggested structure:

```text
src/
  app/
    layout.tsx                 # Global layout (VIGILANT shell)
    page.tsx                   # Dashboard/home (use case selection)
    pcaps/
      page.tsx                 # PCAP list (Network Traces)
      [pcapId]/
        page.tsx               # PCAP detail + investigations list
    investigations/
      [investigationId]/
        page.tsx               # Investigation workspace (chat + report panel)
    reports/
      page.tsx                 # Investigations & reports overview
    search/
      page.tsx                 # RAG search page
    settings/
      page.tsx                 # Backend connection settings
  lib/
    apiClient.ts               # Backend calls, base URL + auth
    config.ts                  # Load/save backend URL and API key
  components/
    layout/
      AppShell.tsx             # Wraps sidebar + top bar + main content
      Sidebar.tsx
      TopBar.tsx
    common/
      Button.tsx
      Card.tsx
      Tag.tsx
      Spinner.tsx
      Modal.tsx
      MarkdownRenderer.tsx
      JsonViewer.tsx
      Badge.tsx
      ErrorAlert.tsx
    pcaps/
      PcapListTable.tsx
      PcapUploadModal.tsx
      PcapSummaryCard.tsx
    investigations/
      InvestigationList.tsx
      InvestigationHeader.tsx
      InvestigationWorkspace.tsx
      MessageBubble.tsx
      ToolMessageCard.tsx
      ChatInput.tsx
      ReportPanel.tsx
    search/
      RagSearchForm.tsx
      RagResultsList.tsx
    settings/
      SettingsForm.tsx
```

The `layout.tsx` component is responsible for:

- Applying the VIGILANT branding (logo/name).
- Rendering the sidebar navigation.
- Rendering the top bar.
- Wrapping all inner pages.

### 7.2 API Client Behavior

`src/lib/apiClient.ts` encapsulates all HTTP calls to the VIGILANT backend. It uses the configuration from `src/lib/config.ts`, which in turn reads/writes:

- `backendUrl`
- `apiKey`

from `localStorage` on the client side.

The API client exports functions such as:

- `listPcaps()`
- `uploadPcap(file: File)`
- `getPcap(pcapId: string)`
- `listInvestigations(params)`
- `createInvestigation(pcapId: string, title?: string)`
- `getInvestigationMessages(id: string)`
- `sendInvestigationMessage(id: string, text: string)`
- `getInvestigationReport(id: string)`
- `generateInvestigationReport(id: string)`
- `queryRagReports(query: string, topK: number)`

All page components call these functions instead of using `fetch` directly, so backend integration is centralized.

### 7.3 Next.js Data Fetching

For pages that need initial data:

- Use **server components** for static or server-side rendering where appropriate:
  - For example, `pcaps/page.tsx` may fetch the list of PCAPs on the server.
- For interactive flows (e.g., sending messages in an investigation):
  - Use client components and call the API client from the browser.
  - Show loading and error states via spinners and alerts.

---

## 8. Error Handling and Loading States

Each page in the VIGILANT Web UI must:

- Display a loading spinner or skeleton while data is being fetched.
- Show concise error messages if API calls fail (connection issues, 4xx/5xx responses).
- Provide basic recovery actions, such as:
  - "Retry" buttons.
  - Link or hint to open **Settings** if backend configuration is likely incorrect.

For example:

- If `GET /health` fails in Settings → show "Cannot reach VIGILANT backend. Check URL or network."
- If `GET /pcaps` fails → show an error card with "Retry" button.

---

## 9. VIGILANT Branding

The name **VIGILANT** appears:

- In the top bar (e.g., "VIGILANT - Cyber Investigation Console").
- In the browser tab title (`<title>VIGILANT</title>` or equivalent Next.js head configuration).
- On the dashboard/landing page (e.g., "Welcome to VIGILANT").

No specific logo is required in the MVP, but:

- Use a consistent font and color accent for the VIGILANT brand (e.g., a primary color used in the sidebar and top bar).
- Ensure the name is clearly visible in all main views so users know they are within the VIGILANT console.

---

This specification describes how the VIGILANT Web UI must be structured to support multiple cybersecurity use cases, with the initial **Network Traces (PCAP)** use case implemented in detail. Future use cases can plug into the same layout, navigation, and backend integration patterns while introducing their own domain-specific pages and components.
