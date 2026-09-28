import {
  Activity,
  Brain,
  CheckCircle2,
  Clock3,
  Database,
  GitBranch,
  ShieldAlert,
  Sparkles,
  XCircle,
} from "lucide-react";

function App() {
  return (
    <div className="app">
      <header className="header">
        <div className="brand">
          <div className="brand-icon">
            <Brain size={24} />
          </div>

          <div>
            <h1>DeployMind</h1>
            <p>Self-Learning DevOps Pipeline Agent</p>
          </div>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          System Learning
        </div>
      </header>

      <main className="container">

        {/* Overview */}

        <section className="hero">
          <div>
            <p className="eyebrow">DEVOPS INTELLIGENCE</p>

            <h2>
              Deploy with the experience of
              <span> every previous deployment.</span>
            </h2>

            <p className="hero-text">
              DeployMind uses persistent Hindsight memory to recall
              previous deployment failures, successes and lessons
              before recommending actions for a new deployment.
            </p>
          </div>

          <div className="memory-counter">
            <Brain size={28} />
            <strong>2</strong>
            <span>Deployment Experiences</span>
          </div>
        </section>


        {/* Deployment */}

        <section className="grid">

          <div className="card deployment-card">
            <div className="card-header">
              <div>
                <p className="eyebrow">CURRENT DEPLOYMENT</p>
                <h3>DEP-002</h3>
              </div>

              <GitBranch size={22} />
            </div>

            <div className="deployment-info">

              <div className="info-item">
                <span>Service</span>
                <strong>Payment Service</strong>
              </div>

              <div className="info-item">
                <span>Version</span>
                <strong>v2.4.0</strong>
              </div>

              <div className="info-item">
                <span>Environment</span>
                <strong>Production</strong>
              </div>

            </div>

            <div className="changes">
              <span>
                <Database size={14} />
                Database Migration
              </span>

              <span>
                <Activity size={14} />
                Payment API
              </span>

              <span>
                Docker Image
              </span>
            </div>

            <button className="analyze-button">
              <Sparkles size={18} />
              Analyze Deployment
            </button>
          </div>


          {/* Risk */}

          <div className="card risk-card">

            <div className="card-header">
              <div>
                <p className="eyebrow">AI RISK ANALYSIS</p>
                <h3>Deployment Risk</h3>
              </div>

              <ShieldAlert size={24} />
            </div>

            <div className="risk-level">
              <div className="risk-number">HIGH</div>
              <p>
                Historical deployment patterns indicate
                elevated migration risk.
              </p>
            </div>

            <div className="recommendation">

              <strong>AI Recommendation</strong>

              <p>
                Test the database migration in staging and
                execute the migration separately before
                production deployment.
              </p>

            </div>

          </div>

        </section>


        {/* Hindsight */}

        <section className="card memory-card">

          <div className="card-header">

            <div>
              <p className="eyebrow">PERSISTENT MEMORY</p>
              <h3>Hindsight Recall</h3>
            </div>

            <Brain size={24} />

          </div>


          <div className="memory-banner">

            <Brain size={20} />

            <div>
              <strong>2 similar deployment experiences found</strong>

              <p>
                DeployMind recalled historical deployment
                knowledge before analyzing DEP-002.
              </p>
            </div>

          </div>


          <div className="memory-list">

            {/* Failed */}

            <div className="memory-item">

              <div className="memory-icon failed">
                <XCircle size={20} />
              </div>

              <div className="memory-content">

                <div className="memory-title">
                  <strong>DEP-001</strong>

                  <span className="failed-badge">
                    FAILED
                  </span>
                </div>

                <p>
                  Payment Service v2.3.0 failed because
                  of a database migration timeout.
                </p>

                <small>
                  Lesson: Test large database migrations
                  in staging.
                </small>

              </div>

              <div className="similarity">
                91%
                <span>similar</span>
              </div>

            </div>


            {/* Success */}

            <div className="memory-item">

              <div className="memory-icon success">
                <CheckCircle2 size={20} />
              </div>

              <div className="memory-content">

                <div className="memory-title">

                  <strong>DEP-002</strong>

                  <span className="success-badge">
                    SUCCESS
                  </span>

                </div>

                <p>
                  Migration was validated in staging and
                  executed separately.
                </p>

                <small>
                  Lesson: Separate migration from application
                  deployment.
                </small>

              </div>

              <div className="similarity">
                94%
                <span>similar</span>
              </div>

            </div>

          </div>

        </section>


        {/* Learning */}

        <section className="grid">

          <div className="card">

            <div className="card-header">

              <div>
                <p className="eyebrow">LEARNING HISTORY</p>
                <h3>Deployment Experience</h3>
              </div>

              <Clock3 size={22} />

            </div>


            <div className="stats">

              <div>
                <strong>2</strong>
                <span>Experiences</span>
              </div>

              <div>
                <strong>1</strong>
                <span>Successful</span>
              </div>

              <div>
                <strong>1</strong>
                <span>Failed</span>
              </div>

            </div>

          </div>


          <div className="card learning-card">

            <p className="eyebrow">LEARNING LOOP</p>

            <div className="learning-flow">

              <span>Deploy</span>
              <span>→</span>
              <span>Observe</span>
              <span>→</span>
              <span>Learn</span>
              <span>→</span>
              <span>Remember</span>

            </div>

            <p>
              Every deployment outcome becomes experience
              that can influence future recommendations.
            </p>

          </div>

        </section>

      </main>
    </div>
  );
}

export default App;