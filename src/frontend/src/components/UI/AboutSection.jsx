import React from "react";
import { Container, Row, Col } from "reactstrap";
import "@styles/about-section.css";
import aboutImg from "/media/bitcoin.png";

const AboutSection = ({ aboutClass }) => {
  return (
    <section
      className="about__section"
      style={
        aboutClass === "aboutPage"
          ? { marginTop: "0px", backgroundColor:'#fff' }
          : { marginTop: "280px", backgroundColor:'#fff' }
      }
    >
      <Container>
        <Row>
          <Col lg="6" md="6">
            <div className="about__section-content">
              <h4 className="section__subtitle">About Us</h4>
              <h2 className="section__title">Welcome to Histock</h2>
              <p className="section__description">
              Histock is a stock investment platform designed for Vietnamese investors. It is the first investment advisory application in Vietnam that uses AI and Machine Learning to automatically calculate indices quickly and accurately. The system also features an AI chatbot specifically trained for specialized advisory tasks for projects of all sizes.
              </p>

              <div className="about__section-item d-flex align-items-center">
                <p className="section__description d-flex align-items-center gap-2">
                  <i className="ri-checkbox-circle-line"></i> Use API to get data from Vnstock markets 
                </p>

                <p className="section__description d-flex align-items-center gap-2">
                  <i className="ri-checkbox-circle-line"></i> Visualize with chart and statistic easily
                </p>
              </div>

              <div className="about__section-item d-flex align-items-center">
                <p className="section__description d-flex align-items-center gap-2">
                  <i className="ri-checkbox-circle-line"></i> Use Machine Learning for automatic task
                </p>

                <p className="section__description d-flex align-items-center gap-2">
                  <i className="ri-checkbox-circle-line"></i>Build powerful chatbot system apply modern technology
                </p>
              </div>
            </div>
          </Col>

          <Col lg="6" md="6">
            <div className="about__img">
              <img src={aboutImg} alt="" className="w-100" />
            </div>
          </Col>
        </Row>
      </Container>
    </section>
  );
};

export default AboutSection;
