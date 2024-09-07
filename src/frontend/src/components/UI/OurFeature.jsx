import RadarChart from "@components/UI/RadarChart"
import { Container, Row, Col } from "reactstrap";

const OurFeature = ()=>{
    return(
        <section className="about__page-section" style={{backgroundColor:'#fff'}}>
        <Container>
          <Row>
            <Col lg="6" md="6" sm="12">
              <div className="about__page-img">
                {/* <img src={driveImg} alt="" className="w-100 rounded-3" /> */}
                <RadarChart/>;
              </div>
            </Col>

            <Col lg="6" md="6" sm="12">
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
            </Col>
          </Row>
        </Container>
      </section>
    );
};
export default OurFeature;