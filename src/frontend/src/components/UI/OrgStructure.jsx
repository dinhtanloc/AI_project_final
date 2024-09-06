import React from "react";
import { Chart } from "react-google-charts";
import {data} from '@assets/data/organStructure.js'
import { Container, Row, Col } from "reactstrap";
import CommonSection from "@components/UI/CommonSection";
import "@styles/about-section.css";
import "@styles/organstructure.css"


export const options = {
  allowHtml: true,
  size:'large'
};

const OrgStructure=() =>{
    const originalWarn = console.warn;

console.warn = function (...args) {
    const arg = args && args[0];

    if (arg && arg.includes('Attempting to load version \'51\' of Google Charts')) return;

    originalWarn(...args);
};
  return (
    <>
    {/* <CommonSection title="About Us" /> */}

      <section className="about__page-section" style={{backgroundColor:'#fff'}}>
        <Container>
          <Col lg="12" className="mb-5 text-center">
              <h6 className="section__subtitle">See our</h6>
              <h2 className="section__title">Popular Services</h2>
            </Col>
            <Row>
            {/* <Col lg="6" md="6" sm="12"> */}
              <div className="about__page-content">
                <h2 className="section__title">
                We are committed to providing genuine brand vehicles.
                </h2>

                <p className="section__description">
                So far, many reputable automotive brands have partnered with our company, making us one of the trustworthy dealers providing high-quality products. You can rest assured and experience our services.
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
            {/* </Col> */}
          </Row>
          <Row>
            {/* <Col lg="6" md="6" sm="12"> */}
            {/* <h4 className="section__subtitle">About Us</h4> */}
            {/* <h2 className="section__title">Welcome to Histock</h2> */}
              <div className="about__page-img">
                {/* <img src={driveImg} alt="" className="w-100 rounded-3" /> */}
                <div className="w-100 rounded-3">
                  

                <div style={{
                      display: 'flex',
                      justifyContent: 'center', /* Canh giữa theo chiều ngang */
                      alignItems: 'center', /* Canh giữa theo chiều dọc (nếu cần) */
                      // height: '400px', /* Hoặc chiều cao của container */
                    }}>
                  <div id="chart_div" style={{marginLeft:'40%'}}>
                    <Chart
                      chartType="OrgChart"
                      data={data}
                      options={options}
                      width="50vw"
                      height="400px"
                    />

                  </div>
                </div>
                </div>
              </div>
            {/* </Col> */}
            </Row>
        </Container>
      </section>
    </>

   
  );
}
export default OrgStructure