import React from "react";

import CommonSection from "@components/UI/CommonSection";
import Helmet from "@components/Helmet/Helmet";
import AboutSection from "@components/UI/AboutSection";
import { Container, Row, Col } from "reactstrap";
import BecomeOurCustomer from "@components/UI/BecomeOurCustomer";

import driveImg from "@assets/all-images/drive.jpg";
import OurMembers from "@components/UI/OurMembers";
import "@styles/about.css";
import OrgStructure from '@components/UI/OrgStructure';
import OurFeature from "@components/UI/OurFeature";
const About = () => {
  return (
    <Helmet title="About">
      <CommonSection title="About Us" />
      <AboutSection aboutClass="aboutPage" />

      <section className="about__page-section" style={{backgroundColor:'#fff'}}>
        <Container>
          <Row>
            <Col lg="6" md="6" sm="12">
              <div className="about__page-img">
                <img src={driveImg} alt="" className="w-100 rounded-3" />
              </div>
            </Col>

            <Col lg="6" md="6" sm="12">
              <div className="about__page-content">
                <h2 className="section__title">
                Our mission is to help you have a safe and effective stock investment journey.
                </h2>

                <p className="section__description">
                In reality, in the Vietnamese market, 95% of investors fail due to a lack of experience and being driven by "herd mentality," which leads to losses and an inability to learn from their mistakes. Histock was created as a mentor to guide you and serve as a compass, directing you towards successful investment strategies.
                </p>

                <p className="section__description">
                Our customers come from all around the world. The value we deliver to your hands is our mission. Customer satisfaction is what our company strives for.
                </p>

                <div className=" d-flex align-items-center gap-3 mt-4">
                  <span className="fs-4">
                    <i className="ri-phone-line"></i>
                  </span>

                  <div>
                    <h6 className="section__subtitle">Need Any Help?</h6>
                    <h4>+0938922810</h4>
                  </div>
                </div>
              </div>
            </Col>
          </Row>
        </Container>
      </section>

      <OrgStructure />
      
      <OurFeature/>

      {/* <BecomeOurCustomer /> */}

      <section>
        <Container>
          <Row>
            <Col lg="12" className="mb-5 text-center">
              <h6 className="section__subtitle">Experts</h6>
              <h2 className="section__title">Our Members</h2>
            </Col>
            <OurMembers />
          </Row>
        </Container>
      </section>
    </Helmet>
  );
};

export default About;