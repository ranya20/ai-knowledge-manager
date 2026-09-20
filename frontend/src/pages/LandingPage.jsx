import { useNavigate } from "react-router-dom"
import { 
  Brain, MessageSquare, FolderOpen, BarChart3, ArrowRight, 
  Upload, FileText, Image, Link, Globe, Search, Bot, 
  Sparkles, Clock, Shield, CheckCircle, Menu, X,
  Zap, Cpu, Database, Cloud, Lock, Target
} from 'lucide-react'
import { useState, useEffect } from "react"
import girlImage from '../../girl.png'
import girl2Image from '../../girl2.png'

export default function LandingPage() {
  const navigate = useNavigate()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const handleGetStarted = () => {
    localStorage.setItem('hasVisited', 'true')
    navigate("/chat")
  }

  return (
    <div style={styles.container}>
      {/* Background avec glow orange */}
      <div style={styles.animatedBg}>
        <div style={styles.glowOrb1}></div>
        <div style={styles.glowOrb2}></div>
        <div style={styles.glowOrb3}></div>
      </div>

      {/* Navbar flottante */}
      <nav style={{...styles.navbar, ...(scrolled ? styles.navbarScrolled : {})}}>
        <div style={styles.navContainer}>
          <div style={styles.logo}>
            <Brain size={32} color="#FF8A00" />
            <span style={styles.logoText}>StudyMind AI</span>
          </div>
          
          <div style={styles.navLinks}>
            <a href="#home" style={styles.navLink}>Home</a>
            <a href="#features" style={styles.navLink}>Features</a>
            <a href="#how-it-works" style={styles.navLink}>How it Works</a>
            <a href="#benefits" style={styles.navLink}>Benefits</a>
            <button style={styles.navCta} onClick={handleGetStarted}>Start Learning</button>
          </div>

          <button style={styles.menuBtn} onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {mobileMenuOpen && (
          <div style={styles.mobileMenu}>
            <a href="#home" style={styles.mobileNavLink}>Home</a>
            <a href="#features" style={styles.mobileNavLink}>Features</a>
            <a href="#how-it-works" style={styles.mobileNavLink}>How it Works</a>
            <a href="#benefits" style={styles.mobileNavLink}>Benefits</a>
            <button style={styles.mobileNavCta} onClick={handleGetStarted}>Start Learning</button>
          </div>
        )}
      </nav>

      {/* Hero Section */}
      <section id="home" style={styles.hero}>
        <div style={styles.heroContent}>
          <div style={styles.heroLeft}>
            <div style={styles.badge}>
              <Sparkles size={16} />
              <span>AI-Powered Learning Platform</span>
            </div>
            <h1 style={styles.heroTitle}>
              Transform Your Study Materials Into an{" "}
              <span style={styles.gradientText}>AI Learning Assistant</span>
            </h1>
            <p style={styles.heroSubtitle}>
              Upload PDFs, scanned notes, images, and website links. Our AI organizes, 
              understands, and answers your questions using your own knowledge base.
            </p>
            <div style={styles.heroButtons}>
              <button style={styles.primaryBtn} onClick={handleGetStarted}>
                Commencer <ArrowRight size={18} style={{ marginLeft: '8px' }} />
              </button>
            </div>
          </div>

          <div style={styles.heroRight}>
            <div style={styles.heroImageContainer}>
              <img 
                src={girlImage} 
                alt="Student with laptop"
                style={styles.studentImage}
              />
              
              {/* Floating Icons with lightning effect */}
              <div style={styles.floatingIcon1}><Zap size={28} color="#FF8A00" /></div>
              <div style={styles.floatingIcon2}><Cpu size={28} color="#FF8A00" /></div>
              <div style={styles.floatingIcon3}><Database size={28} color="#FF8A00" /></div>
              <div style={styles.floatingIcon4}><Cloud size={28} color="#FF8A00" /></div>
              <div style={styles.floatingIcon5}><Lock size={28} color="#FF8A00" /></div>
              <div style={styles.floatingIcon6}><Target size={28} color="#FF8A00" /></div>
              <div style={styles.floatingIcon7}><Bot size={28} color="#FF8A00" /></div>
              <div style={styles.floatingIcon8}><Brain size={28} color="#FF8A00" /></div>
            </div>
          </div>
        </div>
      </section>

      {/* Why StudyMind AI Section */}
      <section id="about" style={styles.section}>
        <div style={styles.sectionContainer}>
          <div style={styles.aboutContent}>
            <div style={styles.aboutLeft}>
              <span style={styles.sectionBadge}>Why Choose Us</span>
              <h2 style={styles.sectionTitle}>Why StudyMind AI?</h2>
              <p style={styles.sectionText}>
                Students waste countless hours searching manually inside PDFs and notes. 
                StudyMind AI centralizes all your resources and creates an intelligent AI tutor 
                that understands your unique learning materials.
              </p>
              <div style={styles.aboutFeatures}>
                <div style={styles.aboutFeature}><CheckCircle size={20} color="#FF8A00" /> Save 70% of study time</div>
                <div style={styles.aboutFeature}><CheckCircle size={20} color="#FF8A00" /> Access anywhere, anytime</div>
                <div style={styles.aboutFeature}><CheckCircle size={20} color="#FF8A00" /> 100% private & secure</div>
              </div>
            </div>
            <div style={styles.aboutRight}>
              <div style={styles.smallImageContainer}>
                <img 
                  src={girl2Image} 
                  alt="Student" 
                  style={styles.smallImage}
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" style={styles.sectionWhite}>
        <div style={styles.sectionContainer}>
          <div style={styles.sectionHeader}>
            <span style={styles.sectionBadge}>Features</span>
            <h2 style={styles.sectionTitleDark}>Everything You Need to Succeed</h2>
            <p style={styles.sectionSubtitleDark}>Powerful tools to transform how you learn and research</p>
          </div>

          <div style={styles.featuresGrid}>
            <div style={styles.featureCardWhite}>
              <div style={styles.featureIcon}><Upload size={32} color="#FF8A00" /></div>
              <h3 style={styles.featureTitleDark}>PDF Upload</h3>
              <p style={styles.featureDescDark}>Import lecture notes, books, summaries, and any PDF document</p>
            </div>

            <div style={styles.featureCardWhite}>
              <div style={styles.featureIcon}><Image size={32} color="#FF8A00" /></div>
              <h3 style={styles.featureTitleDark}>Image OCR</h3>
              <p style={styles.featureDescDark}>Extract text from scanned images and handwritten content</p>
            </div>

            <div style={styles.featureCardWhite}>
              <div style={styles.featureIcon}><Globe size={32} color="#FF8A00" /></div>
              <h3 style={styles.featureTitleDark}>Website Scraping</h3>
              <p style={styles.featureDescDark}>Convert educational websites into structured knowledge</p>
            </div>

            <div style={styles.featureCardWhite}>
              <div style={styles.featureIcon}><Search size={32} color="#FF8A00" /></div>
              <h3 style={styles.featureTitleDark}>Smart RAG Search</h3>
              <p style={styles.featureDescDark}>Find relevant information instantly across all your documents</p>
            </div>

            <div style={styles.featureCardWhite}>
              <div style={styles.featureIcon}><Bot size={32} color="#FF8A00" /></div>
              <h3 style={styles.featureTitleDark}>AI Chatbot</h3>
              <p style={styles.featureDescDark}>Ask questions naturally and get accurate answers from your materials</p>
            </div>

            <div style={styles.featureCardWhite}>
              <div style={styles.featureIcon}><Brain size={32} color="#FF8A00" /></div>
              <h3 style={styles.featureTitleDark}>Personalized Learning</h3>
              <p style={styles.featureDescDark}>Your private academic assistant that adapts to your needs</p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" style={styles.section}>
        <div style={styles.sectionContainer}>
          <div style={styles.sectionHeader}>
            <span style={styles.sectionBadge}>Simple Process</span>
            <h2 style={styles.sectionTitle}>How It Works</h2>
            <p style={styles.sectionSubtitle}>Get started in 4 simple steps</p>
          </div>

          <div style={styles.stepsContainer}>
            <div style={styles.step}>
              <div style={styles.stepNumber}>1</div>
              <div style={styles.stepIcon}><Upload size={32} color="#FF8A00" /></div>
              <h3 style={styles.stepTitle}>Upload Documents</h3>
              <p style={styles.stepDesc}>Add PDFs, images, or website links to your knowledge base</p>
            </div>
            <div style={styles.stepArrow}>→</div>
            <div style={styles.step}>
              <div style={styles.stepNumber}>2</div>
              <div style={styles.stepIcon}><Link size={32} color="#FF8A00" /></div>
              <h3 style={styles.stepTitle}>Add Website Links</h3>
              <p style={styles.stepDesc}>Include online resources and research papers</p>
            </div>
            <div style={styles.stepArrow}>→</div>
            <div style={styles.step}>
              <div style={styles.stepNumber}>3</div>
              <div style={styles.stepIcon}><Brain size={32} color="#FF8A00" /></div>
              <h3 style={styles.stepTitle}>AI Processes Content</h3>
              <p style={styles.stepDesc}>Our AI analyzes and organizes your materials</p>
            </div>
            <div style={styles.stepArrow}>→</div>
            <div style={styles.step}>
              <div style={styles.stepNumber}>4</div>
              <div style={styles.stepIcon}><MessageSquare size={32} color="#FF8A00" /></div>
              <h3 style={styles.stepTitle}>Chat With Your Tutor</h3>
              <p style={styles.stepDesc}>Ask questions and get instant answers</p>
            </div>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section id="benefits" style={styles.sectionWhite}>
        <div style={styles.sectionContainer}>
          <div style={styles.sectionHeader}>
            <span style={styles.sectionBadge}>Benefits</span>
            <h2 style={styles.sectionTitleDark}>Why Students Love StudyMind AI</h2>
          </div>

          <div style={styles.benefitsGrid}>
            <div style={styles.benefitCardWhite}><Clock size={24} color="#FF8A00" /><h4>Save Study Time</h4><p>Reduce research time by 70%</p></div>
            <div style={styles.benefitCardWhite}><BarChart3 size={24} color="#FF8A00" /><h4>Faster Revision</h4><p>Review key concepts quickly</p></div>
            <div style={styles.benefitCardWhite}><Brain size={24} color="#FF8A00" /><h4>Better Understanding</h4><p>AI explains complex topics</p></div>
            <div style={styles.benefitCardWhite}><FolderOpen size={24} color="#FF8A00" /><h4>Centralized Knowledge</h4><p>All resources in one place</p></div>
            <div style={styles.benefitCardWhite}><Shield size={24} color="#FF8A00" /><h4>Reliable Answers</h4><p>Based on your documents only</p></div>
            <div style={styles.benefitCardWhite}><Sparkles size={24} color="#FF8A00" /><h4>Personalized Education</h4><p>Adapts to your learning style</p></div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer style={styles.footer}>
        <div style={styles.footerContainer}>
          <div style={styles.footerContent}>
            <div style={styles.footerLogo}>
              <Brain size={24} color="#FF8A00" />
              <span>StudyMind AI</span>
            </div>
            <p style={styles.footerText}>Transform your study materials into an AI learning assistant</p>
          </div>
          <div style={styles.footerBottom}>
            <p>© 2026 StudyMind AI. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

const styles = {
  container: {
    minHeight: "100vh",
    background: "#FFFFFF",
    color: "#111111",
    position: "relative",
    overflowX: "hidden"
  },
  animatedBg: {
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    overflow: "hidden",
    zIndex: 0
  },
  glowOrb1: {
    position: "absolute",
    top: "10%",
    left: "-10%",
    width: "500px",
    height: "500px",
    background: "radial-gradient(circle, rgba(255,138,0,0.15) 0%, transparent 70%)",
    borderRadius: "50%",
    filter: "blur(60px)",
    animation: "float 20s ease-in-out infinite"
  },
  glowOrb2: {
    position: "absolute",
    bottom: "10%",
    right: "-10%",
    width: "600px",
    height: "600px",
    background: "radial-gradient(circle, rgba(255,167,38,0.1) 0%, transparent 70%)",
    borderRadius: "50%",
    filter: "blur(80px)",
    animation: "float 25s ease-in-out infinite reverse"
  },
  glowOrb3: {
    position: "absolute",
    top: "50%",
    left: "50%",
    width: "400px",
    height: "400px",
    background: "radial-gradient(circle, rgba(255,111,0,0.08) 0%, transparent 70%)",
    borderRadius: "50%",
    filter: "blur(50px)",
    transform: "translate(-50%, -50%)"
  },
  navbar: {
    position: "fixed",
    top: 20,
    left: "50%",
    transform: "translateX(-50%)",
    width: "90%",
    maxWidth: "1200px",
    background: "rgba(255, 255, 255, 0.95)",
    backdropFilter: "blur(10px)",
    borderRadius: "60px",
    padding: "12px 24px",
    zIndex: 1000,
    transition: "all 0.3s ease",
    boxShadow: "0 4px 20px rgba(0,0,0,0.1)",
    border: "1px solid rgba(0,0,0,0.05)"
  },
  navbarScrolled: {
    top: 10,
    background: "rgba(255, 255, 255, 0.98)",
    boxShadow: "0 8px 30px rgba(0,0,0,0.15)"
  },
  navContainer: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center"
  },
  logo: {
    display: "flex",
    alignItems: "center",
    gap: "10px"
  },
  logoText: {
    fontSize: "20px",
    fontWeight: "700",
    color: "#111111"
  },
  navLinks: {
    display: "flex",
    gap: "32px",
    alignItems: "center"
  },
  navLink: {
    color: "#555",
    textDecoration: "none",
    fontSize: "14px",
    fontWeight: "500",
    transition: "color 0.3s ease",
    cursor: "pointer"
  },
  navCta: {
    background: "#FF8A00",
    color: "white",
    border: "none",
    padding: "10px 24px",
    borderRadius: "40px",
    fontSize: "14px",
    fontWeight: "600",
    cursor: "pointer",
    transition: "all 0.3s ease"
  },
  menuBtn: {
    display: "none",
    background: "none",
    border: "none",
    cursor: "pointer"
  },
  mobileMenu: {
    display: "none",
    flexDirection: "column",
    gap: "16px",
    marginTop: "20px",
    paddingTop: "20px",
    borderTop: "1px solid #eee"
  },
  mobileNavLink: {
    color: "#555",
    textDecoration: "none",
    fontSize: "16px"
  },
  mobileNavCta: {
    background: "#FF8A00",
    color: "white",
    border: "none",
    padding: "12px",
    borderRadius: "40px",
    fontSize: "16px",
    fontWeight: "600",
    cursor: "pointer"
  },
  hero: {
    padding: "120px 5% 80px",
    position: "relative",
    zIndex: 1
  },
  heroContent: {
    maxWidth: "1200px",
    margin: "0 auto",
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "60px",
    alignItems: "center"
  },
  badge: {
    display: "inline-flex",
    alignItems: "center",
    gap: "8px",
    background: "rgba(255,138,0,0.1)",
    padding: "8px 16px",
    borderRadius: "40px",
    marginBottom: "24px",
    fontSize: "14px",
    fontWeight: "500",
    color: "#FF8A00"
  },
  heroTitle: {
    fontSize: "48px",
    fontWeight: "700",
    lineHeight: "1.2",
    marginBottom: "24px",
    color: "#111111"
  },
  gradientText: {
    background: "linear-gradient(135deg, #FF8A00, #FFA726)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent"
  },
  heroSubtitle: {
    fontSize: "18px",
    lineHeight: "1.6",
    color: "#555",
    marginBottom: "32px"
  },
  heroButtons: {
    display: "flex",
    gap: "16px",
    marginBottom: "48px"
  },
  primaryBtn: {
    background: "#FF8A00",
    color: "white",
    border: "none",
    padding: "14px 32px",
    borderRadius: "50px",
    fontSize: "16px",
    fontWeight: "600",
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    transition: "all 0.3s ease"
  },
  heroRight: {
    position: "relative"
  },
  heroImageContainer: {
    position: "relative",
    display: "flex",
    justifyContent: "center",
    alignItems: "center"
  },
  studentImage: {
    width: "100%",
    maxWidth: "400px",
    height: "auto",
    borderRadius: "30px",
    boxShadow: "0 20px 60px rgba(0,0,0,0.15)",
    objectFit: "cover"
  },
  floatingIcon1: {
    position: "absolute",
    top: "5%",
    left: "0%",
    background: "white",
    padding: "12px",
    borderRadius: "16px",
    boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
    animation: "float 3s ease-in-out infinite"
  },
  floatingIcon2: {
    position: "absolute",
    bottom: "10%",
    right: "0%",
    background: "white",
    padding: "12px",
    borderRadius: "16px",
    boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
    animation: "float 3s ease-in-out infinite 1s"
  },
  floatingIcon3: {
    position: "absolute",
    top: "30%",
    right: "-5%",
    background: "white",
    padding: "12px",
    borderRadius: "16px",
    boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
    animation: "float 3s ease-in-out infinite 2s"
  },
  floatingIcon4: {
    position: "absolute",
    bottom: "30%",
    left: "-5%",
    background: "white",
    padding: "12px",
    borderRadius: "16px",
    boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
    animation: "float 3s ease-in-out infinite 0.5s"
  },
  floatingIcon5: {
    position: "absolute",
    top: "50%",
    left: "-10%",
    background: "white",
    padding: "12px",
    borderRadius: "16px",
    boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
    animation: "float 3s ease-in-out infinite 1.5s"
  },
  floatingIcon6: {
    position: "absolute",
    bottom: "15%",
    right: "-10%",
    background: "white",
    padding: "12px",
    borderRadius: "16px",
    boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
    animation: "float 3s ease-in-out infinite 2.5s"
  },
  floatingIcon7: {
    position: "absolute",
    top: "15%",
    right: "10%",
    background: "white",
    padding: "12px",
    borderRadius: "16px",
    boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
    animation: "float 3s ease-in-out infinite 0.8s"
  },
  floatingIcon8: {
    position: "absolute",
    bottom: "40%",
    left: "10%",
    background: "white",
    padding: "12px",
    borderRadius: "16px",
    boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
    animation: "float 3s ease-in-out infinite 1.8s"
  },
  section: {
    padding: "80px 5%",
    position: "relative",
    zIndex: 1,
    background: "#FFFFFF"
  },
  sectionWhite: {
    padding: "80px 5%",
    background: "#F8F9FC",
    position: "relative",
    zIndex: 1
  },
  sectionContainer: {
    maxWidth: "1200px",
    margin: "0 auto"
  },
  sectionHeader: {
    textAlign: "center",
    marginBottom: "60px"
  },
  sectionBadge: {
    display: "inline-block",
    background: "rgba(255,138,0,0.1)",
    color: "#FF8A00",
    padding: "6px 14px",
    borderRadius: "20px",
    fontSize: "14px",
    fontWeight: "500",
    marginBottom: "16px"
  },
  sectionTitle: {
    fontSize: "36px",
    fontWeight: "700",
    marginBottom: "16px",
    color: "#111111"
  },
  sectionTitleDark: {
    fontSize: "36px",
    fontWeight: "700",
    marginBottom: "16px",
    color: "#111111"
  },
  sectionSubtitle: {
    fontSize: "18px",
    color: "#555",
    maxWidth: "600px",
    margin: "0 auto"
  },
  sectionSubtitleDark: {
    fontSize: "18px",
    color: "#555",
    maxWidth: "600px",
    margin: "0 auto"
  },
  sectionText: {
    fontSize: "16px",
    lineHeight: "1.6",
    color: "#555",
    marginBottom: "24px"
  },
  aboutContent: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "60px",
    alignItems: "center"
  },
  aboutFeatures: {
    display: "flex",
    flexDirection: "column",
    gap: "12px"
  },
  aboutFeature: {
    display: "flex",
    alignItems: "center",
    gap: "12px",
    fontSize: "16px",
    color: "#111111"
  },
  aboutRight: {
    display: "flex",
    justifyContent: "center"
  },
  smallImageContainer: {
    width: "300px",
    height: "300px",
    borderRadius: "20px",
    overflow: "hidden",
    boxShadow: "0 10px 30px rgba(0,0,0,0.1)"
  },
  smallImage: {
    width: "100%",
    height: "100%",
    objectFit: "cover"
  },
  featuresGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(350px, 1fr))",
    gap: "30px"
  },
  featureCardWhite: {
    background: "#FFFFFF",
    borderRadius: "24px",
    padding: "32px",
    transition: "all 0.3s ease",
    cursor: "pointer",
    boxShadow: "0 4px 20px rgba(0,0,0,0.08)",
    border: "1px solid rgba(0,0,0,0.05)"
  },
  featureIcon: {
    marginBottom: "20px"
  },
  featureTitleDark: {
    fontSize: "20px",
    fontWeight: "600",
    marginBottom: "12px",
    color: "#111111"
  },
  featureDescDark: {
    fontSize: "14px",
    color: "#555",
    lineHeight: "1.5"
  },
  stepsContainer: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    flexWrap: "wrap",
    gap: "20px"
  },
  step: {
    flex: 1,
    textAlign: "center",
    padding: "30px",
    background: "#FFFFFF",
    borderRadius: "24px",
    position: "relative",
    boxShadow: "0 4px 20px rgba(0,0,0,0.08)",
    border: "1px solid rgba(0,0,0,0.05)"
  },
  stepNumber: {
    position: "absolute",
    top: "-15px",
    left: "50%",
    transform: "translateX(-50%)",
    background: "#FF8A00",
    width: "30px",
    height: "30px",
    borderRadius: "50%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: "700",
    color: "white"
  },
  stepIcon: {
    marginBottom: "16px"
  },
  stepTitle: {
    fontSize: "18px",
    fontWeight: "600",
    marginBottom: "8px",
    color: "#111111"
  },
  stepDesc: {
    fontSize: "14px",
    color: "#555"
  },
  stepArrow: {
    fontSize: "24px",
    color: "#FF8A00"
  },
  benefitsGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
    gap: "24px"
  },
  benefitCardWhite: {
    background: "#FFFFFF",
    borderRadius: "20px",
    padding: "24px",
    textAlign: "center",
    boxShadow: "0 4px 20px rgba(0,0,0,0.08)",
    border: "1px solid rgba(0,0,0,0.05)",
    transition: "all 0.3s ease"
  },
  footer: {
    background: "#F8F9FC",
    padding: "60px 5% 30px",
    position: "relative",
    zIndex: 1,
    borderTop: "1px solid rgba(0,0,0,0.05)"
  },
  footerContainer: {
    maxWidth: "1200px",
    margin: "0 auto"
  },
  footerContent: {
    textAlign: "center",
    marginBottom: "40px"
  },
  footerLogo: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: "10px",
    marginBottom: "16px"
  },
  footerText: {
    color: "#555",
    fontSize: "14px"
  },
  footerBottom: {
    textAlign: "center",
    paddingTop: "30px",
    borderTop: "1px solid rgba(0,0,0,0.1)",
    color: "#555",
    fontSize: "12px"
  }
}

// Add responsive styles
const mediaStyles = document.createElement("style")
mediaStyles.textContent = `
  @keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
  }
  
  @media (max-width: 968px) {
    .hero-content {
      grid-template-columns: 1fr !important;
      text-align: center;
    }
    
    .hero-left {
      order: 2;
    }
    
    .hero-buttons {
      justify-content: center;
    }
    
    .nav-links {
      display: none !important;
    }
    
    .menu-btn {
      display: block !important;
    }
    
    .mobile-menu {
      display: flex !important;
    }
    
    .about-content {
      grid-template-columns: 1fr !important;
      text-align: center;
    }
    
    .about-features {
      align-items: center;
    }
    
    .steps-container {
      flex-direction: column;
    }
    
    .step-arrow {
      transform: rotate(90deg);
    }
    
    .hero-title {
      font-size: 36px !important;
    }
  }
  
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  }
  
  html {
    scroll-behavior: smooth;
  }
  
  button:hover {
    transform: translateY(-2px);
    opacity: 0.9;
  }
  
  .feature-card-white:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.12);
  }
  
  .benefit-card-white:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.12);
  }
`
document.head.appendChild(mediaStyles)