import React, { useEffect } from "react";
import { Chart } from "react-google-charts";
import {data} from '@assets/data/organStructure.js'
import { Container, Row, Col } from "reactstrap";
import "@styles/about-section.css";
import "@styles/organstructure.css"


export const options = {
  allowHtml: true,
  size:'large',
  // color:'black'
  // fontColor:'black'
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
              <h2 className="section__title">Company structure</h2>
            </Col>
              <p className="section__description">
              To bring Moketo Gr. to reality, we must acknowledge the dedicated team of the company, comprising passionate young professionals from the fields of technology and innovation at UEH University. Each department plays a crucial role in ensuring the project's success and its positive development.
              </p>

              <p className="section__description">
              To steer the project in the right direction, we must acknowledge the advisory team of professors from UEH University and Saigon University who have supported and participated in the project. Their expertise has guided the project effectively, especially in the challenging field of finance and investment in the stock market, which requires extensive knowledge and experience.
              </p>
            <Row>
            {/* <Col lg="6" md="6" sm="12"> */}
              {/* <div className="about__page-content"> */}
                {/* <h2 className="section__title">
                We are committed to providing genuine brand vehicles.
                </h2> */}


                <div className=" d-flex align-items-center gap-3 mt-4">
                  <span className="fs-4">
                    <i className="ri-phone-line"></i>
                  </span>

                  {/* <div>
                    <h6 className="section__subtitle">Need Any Help?</h6>
                    <h4>+0938922810</h4>
                  </div> */}
                </div>
              {/* </div> */}
            {/* </Col> */}
          </Row>
          <Row>
            {/* <Col lg="6" md="6" sm="12"> */}
            {/* <h4 className="section__subtitle">About Us</h4> */}
            {/* <h2 className="section__title">Welcome to </h2> */}
              <div className="about__page-img">
                {/* <img src={driveImg} alt="" className="w-100 rounded-3" /> */}
                <div className="w-100 rounded-3">
                  

                <div style={{
                      display: 'flex',
                      // justifyContent: 'center', /* Canh giữa theo chiều ngang */
                      // alignItems: 'center', /* Canh giữa theo chiều dọc (nếu cần) */
                      // height: '400px', /* Hoặc chiều cao của container */
                    }}>
                  <div id="chart_div" style={{ color:'black'}}>
                    <Chart
                      chartType="OrgChart"
                      data={data}
                      options={options}
                      // width="80vw"
                      // height="900px"
                      // color='black'
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