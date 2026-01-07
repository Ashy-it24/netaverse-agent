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
      console.log('Analyzing politician:', politician)
      const response = await fetch(`http://localhost:8000/analyze?name=${encodeURIComponent(politician)}`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const result = await response.json()
      console.log('Analysis result:', result)

      if (result.error) {
        setError(result.error)
      } else {
        setData(result)
      }
    } catch (err) {
      console.error('Analysis error:', err)
      setError(`Failed to analyze: ${err.message}. Make sure the backend is running on port 8000.`)
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      analyzePolitician()
    }
  }

  const getImpactColor = (impact) => {
    switch (impact) {
      case 'positive':
        return '#d4edda'
      case 'neutral':
        return '#f8f9fa'
      case 'controversial':
        return '#f8d7da'
      default:
        return '#f8f9fa'
    }
  }

  const getFulfillmentColor = (status) => {
    switch (status) {
      case 'fulfilled':
        return '#d4edda'
      case 'partially_fulfilled':
        return '#fff3cd'
      case 'in_progress':
        return '#cce5ff'
      case 'not_fulfilled':
      case 'broken':
        return '#f8d7da'
      default:
        return '#f8f9fa'
    }
  }

  const getStatusBadge = (status) => {
    const colors = {
      'Passed': '#28a745',
      'Signed into Law': '#28a745',
      'Introduced': '#007bff',
      'Failed': '#dc3545',
      'Vetoed': '#dc3545',
      'In Committee': '#ffc107'
    }
    return colors[status] || '#6c757d'
  }

  const getFulfillmentPercentageColor = (percentage) => {
    if (percentage >= 75) return '#28a745'
    if (percentage >= 50) return '#ffc107'
    if (percentage >= 25) return '#fd7e14'
    return '#dc3545'
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🏛️ Politician Activity Analyzer</h1>
        <p className="subtitle">Comprehensive analysis of political activities, promises, and voting records</p>
        <div className="search-section">
          <input
            type="text"
            placeholder="Enter politician name (e.g., Joe Biden, Narendra Modi)"
            value={politician}
            onChange={(e) => setPolitician(e.target.value)}
            onKeyPress={handleKeyPress}
            className="search-input"
          />
          <button
            onClick={analyzePolitician}
            disabled={loading}
            className="analyze-button"
          >
            {loading ? '🔄 Analyzing...' : '🔍 Analyze'}
          </button>
        </div>
      </header>

      <main className="main">
        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}

        {loading && (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Gathering and analyzing data for {politician}...</p>
          </div>
        )}

        {data && (
          <div className="results">
            {/* Profile Header */}
            <div className="profile-header">
              <div className="profile-info">
                <h2>{data.politician || 'Unknown Politician'}</h2>
                {data.party && <span className="party-badge">{data.party}</span>}
                {data.position && <p className="position">{data.position}</p>}
                {data.term_period && <p className="term">Term: {data.term_period}</p>}
              </div>
              <div className="summary-box">
                <p>{data.summary || 'No summary available.'}</p>
              </div>
            </div>

            {/* Promise Fulfillment Analysis Dashboard */}
            {data.promise_analysis && (
              <section className="analysis-section promise-dashboard">
                <h3>📊 Promise Fulfillment Analysis</h3>
                <div className="dashboard-grid">
                  <div className="metric-card fulfilled">
                    <span className="metric-value">{data.promise_analysis.fulfilled_count || 0}</span>
                    <span className="metric-label">Fulfilled</span>
                  </div>
                  <div className="metric-card partial">
                    <span className="metric-value">{data.promise_analysis.partially_fulfilled_count || 0}</span>
                    <span className="metric-label">Partially Fulfilled</span>
                  </div>
                  <div className="metric-card progress">
                    <span className="metric-value">{data.promise_analysis.in_progress_count || 0}</span>
                    <span className="metric-label">In Progress</span>
                  </div>
                  <div className="metric-card not-fulfilled">
                    <span className="metric-value">{data.promise_analysis.not_fulfilled_count || 0}</span>
                    <span className="metric-label">Not Fulfilled</span>
                  </div>
                </div>
                
                <div className="fulfillment-rate">
                  <div className="rate-header">
                    <span>Overall Fulfillment Rate</span>
                    <span className="rate-value">
                      {data.promise_analysis.calculated_fulfillment_rate || data.promise_analysis.overall_fulfillment_rate || 'N/A'}
                    </span>
                  </div>
                  <div className="progress-bar-container">
                    <div 
                      className="progress-bar-fill"
                      style={{ 
                        width: `${parseFloat(data.promise_analysis.calculated_fulfillment_rate || data.promise_analysis.overall_fulfillment_rate || 0)}%`,
                        backgroundColor: getFulfillmentPercentageColor(parseFloat(data.promise_analysis.calculated_fulfillment_rate || 0))
                      }}
                    ></div>
                  </div>
                </div>

                {data.promise_analysis.analysis_summary && (
                  <div className="analysis-summary">
                    <p>{data.promise_analysis.analysis_summary}</p>
                  </div>
                )}

                <div className="strength-weakness">
                  {data.promise_analysis.strongest_areas && data.promise_analysis.strongest_areas.length > 0 && (
                    <div className="strength-box">
                      <h4>✅ Strongest Areas</h4>
                      <ul>
                        {data.promise_analysis.strongest_areas.map((area, i) => (
                          <li key={i}>{area}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {data.promise_analysis.weakest_areas && data.promise_analysis.weakest_areas.length > 0 && (
                    <div className="weakness-box">
                      <h4>⚠️ Areas Needing Improvement</h4>
                      <ul>
                        {data.promise_analysis.weakest_areas.map((area, i) => (
                          <li key={i}>{area}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </section>
            )}

            <div className="analysis-sections">
              {/* Recent Activities */}
              <section className="analysis-section">
                <h3>📰 Recent Activities</h3>
                {data.activities && data.activities.length > 0 ? (
                  <div className="activities-grid">
                    {data.activities.map((activity, index) => (
                      <div
                        key={index}
                        className="activity-card"
                        style={{ borderLeft: `4px solid ${getImpactColor(activity.impact) === '#d4edda' ? '#28a745' : getImpactColor(activity.impact) === '#f8d7da' ? '#dc3545' : '#6c757d'}` }}
                      >
                        <div className="card-header">
                          <span className="category-badge">{activity.category || 'General'}</span>
                          {activity.date && <span className="date-badge">{activity.date}</span>}
                        </div>
                        <p className="activity-text">{activity.activity || 'No description available'}</p>
                        {activity.details && <p className="activity-details">{activity.details}</p>}
                        <div className="impact-badge" style={{ backgroundColor: getImpactColor(activity.impact || 'neutral') }}>
                          Impact: {activity.impact || 'neutral'}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="no-data">
                    <p>No recent activities found for this politician.</p>
                  </div>
                )}
              </section>

              {/* Manifesto Promises */}
              <section className="analysis-section">
                <h3>📜 Manifesto Promises & Fulfillment Status</h3>
                {data.promises && data.promises.length > 0 ? (
                  <div className="promises-grid">
                    {data.promises.map((promise, index) => (
                      <div
                        key={index}
                        className="promise-card"
                        style={{ borderTop: `4px solid ${getFulfillmentColor(promise.status) === '#d4edda' ? '#28a745' : getFulfillmentColor(promise.status) === '#f8d7da' ? '#dc3545' : getFulfillmentColor(promise.status) === '#cce5ff' ? '#007bff' : '#ffc107'}` }}
                      >
                        <div className="promise-header">
                          <span 
                            className="status-badge"
                            style={{ backgroundColor: getFulfillmentColor(promise.status || 'unknown') }}
                          >
                            {(promise.status || 'unknown').replace(/_/g, ' ').toUpperCase()}
                          </span>
                          {promise.fulfillment_percentage !== undefined && (
                            <div className="fulfillment-meter">
                              <div 
                                className="meter-fill"
                                style={{ 
                                  width: `${promise.fulfillment_percentage}%`,
                                  backgroundColor: getFulfillmentPercentageColor(promise.fulfillment_percentage)
                                }}
                              ></div>
                              <span className="meter-text">{promise.fulfillment_percentage}%</span>
                            </div>
                          )}
                        </div>
                        <h4 className="promise-title">{promise.promise || 'No promise description'}</h4>
                        {promise.made_during && (
                          <p className="promise-meta">Made during: {promise.made_during}</p>
                        )}
                        <div className="promise-details">
                          <p><strong>📋 Evidence:</strong> {promise.evidence || 'No evidence provided'}</p>
                          {promise.timeline && <p><strong>⏱️ Timeline:</strong> {promise.timeline}</p>}
                          <p><strong>📈 Impact:</strong> {promise.impact || 'Impact not specified'}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="no-data">
                    <p>No promises data found for this politician.</p>
                  </div>
                )}
              </section>

              {/* Bills */}
              <section className="analysis-section">
                <h3>📑 Legislative Record - Bills</h3>
                <div className="bills-grid">
                  {data.bills && data.bills.map((bill, index) => (
                    <div key={index} className="bill-card">
                      <div className="bill-header">
                        <h4>{bill.title}</h4>
                        <span 
                          className="bill-status-badge"
                          style={{ backgroundColor: getStatusBadge(bill.status) }}
                        >
                          {bill.status}
                        </span>
                      </div>
                      {bill.bill_number && <p className="bill-number">Bill #: {bill.bill_number}</p>}
                      <p className="bill-year">Year: {bill.year}</p>
                      <p className="bill-description">{bill.description}</p>
                      <div className="bill-footer">
                        {bill.role && <span className="role-badge">Role: {bill.role}</span>}
                        {bill.impact_area && <span className="area-badge">{bill.impact_area}</span>}
                      </div>
                    </div>
                  ))}
                </div>
              </section>

              {/* Voting Record Summary */}
              {data.voting_record_summary && (
                <section className="analysis-section">
                  <h3>🗳️ Voting Record Summary</h3>
                  {data.voting_record_summary.alignment && (
                    <p className="alignment-text">
                      <strong>Political Alignment:</strong> {data.voting_record_summary.alignment}
                    </p>
                  )}
                  {data.voting_record_summary.key_votes && data.voting_record_summary.key_votes.length > 0 && (
                    <div className="votes-list">
                      {data.voting_record_summary.key_votes.map((vote, index) => (
                        <div key={index} className="vote-item">
                          <span className="vote-issue">{vote.issue}</span>
                          <span className={`vote-position ${vote.position?.toLowerCase()}`}>
                            {vote.position}
                          </span>
                          <span className="vote-year">{vote.year}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </section>
              )}

              {/* Controversies */}
              {data.controversies && data.controversies.length > 0 && (
                <section className="analysis-section controversies-section">
                  <h3>⚡ Notable Controversies</h3>
                  <div className="controversies-list">
                    {data.controversies.map((controversy, index) => (
                      <div key={index} className="controversy-item">
                        <div className="controversy-header">
                          <span className="controversy-year">{controversy.year}</span>
                        </div>
                        <p className="controversy-issue">{controversy.issue}</p>
                        {controversy.resolution && (
                          <p className="controversy-resolution">
                            <strong>Resolution:</strong> {controversy.resolution}
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                </section>
              )}

              {/* Data Sources */}
              {data.data_sources && data.data_sources.length > 0 && (
                <section className="data-sources">
                  <h4>📚 Data Sources</h4>
                  <ul>
                    {data.data_sources.map((source, index) => (
                      <li key={index}>{source}</li>
                    ))}
                  </ul>
                </section>
              )}
            </div>
          </div>
        )}
      </main>

      <footer className="footer">
        <p>Data analyzed using AI. Always verify information from official sources.</p>
      </footer>
    </div>
  )
}

export default App
