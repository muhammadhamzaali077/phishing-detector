const alertsBody = document.getElementById("alerts-body");
const portalStatus = document.getElementById("portal-status");
let knownAlertIds = new Set();

async function fetchAlerts() {
  try {
    const response = await fetch("/alerts");
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const records = await response.json();
    renderAlerts(records);
    checkForNewAlerts(records);
    portalStatus.textContent = `Last updated: ${new Date().toLocaleTimeString()}`;
  } catch (error) {
    portalStatus.textContent = `Unable to load alerts: ${error.message}`;
  }
}

function renderAlerts(records) {
  if (!records.length) {
    alertsBody.innerHTML = '<tr><td colspan="5">No phishing alerts have been detected yet.</td></tr>';
    return;
  }

  alertsBody.innerHTML = records
    .map((record) => {
      const statusClass = record.status === "new" ? "status-new" : "status-viewed";
      return `
        <tr>
          <td>${escapeHtml(record.sender)}</td>
          <td>${escapeHtml(record.subject)}</td>
          <td>${escapeHtml(record.received_at)}</td>
          <td>${escapeHtml(record.detected_at)}</td>
          <td class="${statusClass}">${escapeHtml(record.status)}</td>
        </tr>
      `;
    })
    .join("");
}

function checkForNewAlerts(records) {
  const newAlerts = records.filter((record) => !knownAlertIds.has(record.alert_id));
  for (const record of newAlerts) {
    knownAlertIds.add(record.alert_id);
    if (record.status === "new") {
      window.alert(`New phishing threat detected:\nSender: ${record.sender}\nSubject: ${record.subject}`);
    }
  }
}

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

fetchAlerts();
setInterval(fetchAlerts, 10000);
