import { useState } from 'react';
import { sendQuery } from './api';

function App() {
  const [prompt, setPrompt] = useState('');
  const [responseType, setResponseType] = useState('');
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState([]);
  const [sql, setSql] = useState('');
  const [rawResponse, setRawResponse] = useState('');
  const [results, setResults] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setResponseType('');
    setAnswer('');
    setSources([]);
    setSql('');
    setRawResponse('');
    setResults([]);
    setError('');
    setLoading(true);

    try {
      const response = await sendQuery(prompt);
      setResponseType(response.response_type || '');

      if (response.response_type === 'faq') {
        setAnswer(response.answer || '');
        setSources(response.sources || []);
      } else {
        setSql(response.generated_sql || '');
        setResults(response.rows || []);
        setRawResponse(response.raw_response || '');
      }
    } catch (err) {
      const data = err.response?.data;
      const detail = data?.detail || data;
      setError(
        detail?.error || detail?.detail || (typeof detail === 'string' ? detail : err.message) || 'Request failed'
      );
      setRawResponse(detail?.raw_response || data?.raw_response || '');
      setSql(detail?.sql || '');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ padding: 24, fontFamily: 'Arial, sans-serif', maxWidth: 800, margin: '0 auto' }}>
      <h1>Chatbot</h1>
      <form onSubmit={handleSubmit} style={{ marginBottom: 24 }}>
        <input
          value={prompt}
          onChange={(event) => setPrompt(event.target.value)}
          placeholder="Ask about the E-District system or portal"
          style={{ width: '100%', padding: 12, fontSize: 16, marginBottom: 12 }}
        />
        <button type="submit" disabled={!prompt.trim() || loading} style={{ padding: '12px 18px', fontSize: 16 }}>
          {loading ? 'Generating...' : 'Submit'}
        </button>
      </form>

      {error && (
        <div style={{ marginBottom: 16, color: '#b00020' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {responseType === 'faq' && (
        <section style={{ marginBottom: 24, padding: 16, background: '#f8f9fa', borderRadius: 8 }}>
          <h2 style={{ marginBottom: 12 }}>FAQ Answer</h2>
          <div style={{ marginBottom: 12 }}>
            <strong>Question:</strong>
            <div style={{ marginTop: 6, padding: 12, background: '#ffffff', borderRadius: 6, border: '1px solid #ddd' }}>
              {prompt}
            </div>
          </div>
          <div style={{ marginBottom: 12 }}>
            <strong>Answer:</strong>
            <div style={{ marginTop: 6, padding: 12, background: '#ffffff', borderRadius: 6, border: '1px solid #ddd' }}>
              {answer}
            </div>
          </div>
          {sources.length > 0 && (
            <div>
              <strong>Source:</strong>
              <div style={{ marginTop: 6, padding: 12, background: '#ffffff', borderRadius: 6, border: '1px solid #ddd' }}>
                {sources.join(', ')}
              </div>
            </div>
          )}
        </section>
      )}

      {responseType === 'sql' && (
        <>
          {sql && (
            <section style={{ marginBottom: 24 }}>
              <h2>Generated SQL</h2>
              <pre style={{ background: '#f2f2f2', padding: 12, whiteSpace: 'pre-wrap' }}>{sql}</pre>
            </section>
          )}

          {rawResponse && (
            <section style={{ marginBottom: 24 }}>
              <h2>Raw Model Response</h2>
              <pre style={{ background: '#f8f8f8', padding: 12, whiteSpace: 'pre-wrap' }}>{rawResponse}</pre>
            </section>
          )}

          {results.length > 0 && (
            <section>
              <h2>Results</h2>
              <div style={{ overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                  <thead>
                    <tr>
                      {Object.keys(results[0]).map((key) => (
                        <th key={key} style={{ border: '1px solid #ddd', padding: 8, textAlign: 'left' }}>
                          {key}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {results.map((row, rowIndex) => (
                      <tr key={rowIndex}>
                        {Object.values(row).map((value, cellIndex) => (
                          <td key={cellIndex} style={{ border: '1px solid #ddd', padding: 8 }}>
                            {value === null ? 'NULL' : String(value)}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          )}
        </>
      )}
    </main>
  );
}

export default App;
