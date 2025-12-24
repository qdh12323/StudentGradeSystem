import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
// 如果你想要一些基础样式，可以把下面这行留着；如果没有 index.css 也可以删掉
// import './index.css' 

// #region agent log
const logDebug = (location: string, message: string, data: any, hypothesisId: string) => {
  fetch('http://127.0.0.1:7244/ingest/d70bd03f-0689-4b0f-b937-3c68842f8ea0', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ location, message, data, timestamp: Date.now(), sessionId: 'debug-session', runId: 'run1', hypothesisId })
  }).catch(() => {});
};
// #endregion

// #region agent log
logDebug('main.tsx:17', 'Entry point execution started', { rootElementExists: !!document.getElementById('root') }, 'E');
// #endregion

const rootElement = document.getElementById('root');

// #region agent log
logDebug('main.tsx:21', 'Root element check', { rootElement: rootElement ? 'found' : 'not found' }, 'E');
if (!rootElement) {
  logDebug('main.tsx:23', 'ERROR: Root element not found', {}, 'E');
  throw new Error('Root element not found');
}
// #endregion

// #region agent log
try {
  logDebug('main.tsx:28', 'Creating React root', {}, 'E');
  // #endregion
  const root = ReactDOM.createRoot(rootElement);
  // #region agent log
  logDebug('main.tsx:31', 'React root created, calling render', {}, 'E');
  // #endregion
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
  );
  // #region agent log
  logDebug('main.tsx:38', 'Render call completed', {}, 'E');
} catch (error) {
  logDebug('main.tsx:40', 'ERROR in entry point', { error: error instanceof Error ? error.message : String(error), stack: error instanceof Error ? error.stack : undefined }, 'E');
  console.error('Entry point error:', error);
  // #endregion
}