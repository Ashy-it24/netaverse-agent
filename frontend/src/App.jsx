import { useState } from 'react'
import './App.css'

function App() {
  const [politician, setPolitician] = useState('')
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const analyzePolitician = async () => {
    if (!politician.trim()) return

    setLoading(true)
    setError('')
    setData(null)

    try {
      const response = await fetch(`http://localhost:8000/analyze?name=${encodeURIComponent(politician)}`)
      const result = await response.json()

      if (result.error) {
        setError(result.error)
      } else {
        setData(result)
      }
    } catch (err) {
      setError('Failed to analyze. Make sure the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const getImpactColor = (impact) => {
    switch (impact) {
      case 'positive':
        return '#d4edda' // Light green
      case 'neutral':
        return '#f8f9fa' // Light gray
      case 'controversial':
        return '#f8d7da' // Light red
      default:
        return '#f8f9fa'
    }
  }

  const getFulfillmentColor = (status) => {
    switch (status) {
      case 'fulfilled':
        return '#d4edda' // Light green
      case 'partially_fulfilled':
        return '#fff3cd' // Light yellow
      case 'in_progress':
        return '#cce5ff' // Light blue
      case 'not_fulfilled':
        return '#f8d7da' // Light red
      default:
        return '#f8f9fa' // Light gray
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Politician Activity Analyzer</h1>
        <div className="search-section">
          <input
            type="text"
            placeholder="Enter politician name (e.g., Joe Biden)"
            value={politician}
            onChange={(e) => setPolitician(e.target.value)}
            className="search-input"
          />
          <button
            onClick={analyzePolitician}
            disabled={loading}
            className="analyze-button"
          >
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </div>
      </header>

      <main className="main">
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {data && (
          <div className="results">
            <div className="summary">
              <h2>{data.politician}</h2>
              <p>{data.summary}</p>
            </div>

            <div className="analysis-sections">
              <section className="analysis-section">
                <h3>Recent Activities</h3>
                <div className="activities-grid">
                  {data.activities.map((activity, index) => (
                    <div
                      key={index}
                      className="activity-card"
                      style={{ backgroundColor: getImpactColor(activity.impact) }}
                    >
                      <h4>Activity {index + 1}</h4>
                      <p className="activity-text">{activity.activity}</p>
                      <div className="metadata">
                        <span className="category">Category: {activity.category}</span>
                        <span className="impact">Impact: {activity.impact}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </section>

              <section className="analysis-section">
                <h3>Manifesto Promises & Fulfillment</h3>
                <div className="promises-grid">
                  {data.promises.map((promise, index) => (
                    <div
                      key={index}
                      className="promise-card"
                      style={{ backgroundColor: getFulfillmentColor(promise.status) }}
                    >
                      <h4>Promise {index + 1}</h4>
                      <p className="promise-text">{promise.promise}</p>
                      <div className="metadata">
                        <span className="status">Status: {promise.status.replace('_', ' ')}</span>
                        <p className="evidence"><strong>Evidence:</strong> {promise.evidence}</p>
                        <p className="impact"><strong>Impact:</strong> {promise.impact}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </section>

              <section className="analysis-section">
                <h3>Bills Passed During Term</h3>
                <div className="bills-list">
                  {data.bills.map((bill, index) => (
                    <div key={index} className="bill-item">
                      <h4>{bill.title} ({bill.year})</h4>
                      <p>{bill.description}</p>
                      <span className="bill-status">Status: {bill.status}</span>
                    </div>
                  ))}
                </div>
              </section>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
