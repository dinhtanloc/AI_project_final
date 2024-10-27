import React from "react";

import CommonSection from "@client/components/UI/CommonSection";
import Helmet from "@client/components/Helmet/Helmet";
import AboutSection from "@client/components/UI/AboutSection";
import { Container, Row, Col } from "reactstrap";
import driveImg from "@assets/all-images/upward.png";
import OurMembers from "@client/components/UI/OurMembers";
import "@client/styles/about.css";
import OrgStructure from '@client/components/UI/OrgStructure';
import OurFeature from "@client/components/UI/OurFeature";

// window.location.reload()
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
                <img src={driveImg} alt="" className="w-100 rounded-3" style={{height:'500px'}} />
              </div>
            </Col>

            <Col lg="6" md="6" sm="12">
              <div className="about__page-content">
                <h2 className="section__title">
                Our mission is to help you have a safe and effective stock investment journey.
                </h2>

                <p className="section__description">
                In reality, in the Vietnamese market, 95% of investors fail due to a lack of experience and being driven by "herd mentality," which leads to losses and an inability to learn from their mistakes. Moketo Gr. was created as a mentor to guide you and serve as a compass, directing you towards successful investment strategies.
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
