import React, {useState, useEffect} from "react";
import HeroSlider from "@components/UI/HeroSlider";
import Helmet from "@components/Helmet/Helmet";

import { Container, Row, Col, Form, FormGroup } from "reactstrap";
import AboutSection from "@components/UI/AboutSection";
import ServicesList from "@components/UI/ServicesList";
import BecomeOurCustomer from "@components/UI/BecomeOurCustomer";
import Testimonial from "@components/UI/Testimonial";
import "@styles/find-car-form.css"
import BlogList from "@components/UI/BlogList";

const HomePage = () => {
  const [prompt, setPrompt] = useState('');
  const [color, setColor] = useState('');

  const handleFindCar = async (e) => {
    // e.preventDefault()
    // try {
    //   const combinedPrompt = color ? `${prompt} with ${color}`: prompt;
    //   const response = await instance.post('/categories/find-car/', {
    //     prompt: combinedPrompt,
    //   });
    //   const { products } = response.data;
    //   // Chuyển đến trang CarListing với dữ liệu được lọc
    //   navigate('/cars', { state: { products: products } });
    // } catch (error) {
    //   console.error('There was an error fetching the data!', error);
    // }
  };

  return (
    <Helmet title="Home">
      {/* ============= hero section =========== */}
      <section className="p-0 hero__slider-section">
        <HeroSlider />

        <div className="hero__form">
          <Container>
            <Row className="form__row" >
              <Col lg="4" md="4">
                <div className="find__cars-left">
                  <h2>Find your best ticker here</h2>
                </div>
              </Col>

              <Col lg="5" md="5" sm="12">
                <Form className="form"  onSubmit={handleFindCar}>
                  <div className=" d-flex align-items-center justify-content-between flex-wrap">
                    <FormGroup className="form__group" style={{width:"65%"}}>
                      <input 
                      type="text"
                      value={prompt} 
                      placeholder="What ticket do you want?"
                      onChange={(e) => setPrompt(e.target.value)}
                      required />
                    </FormGroup>

                    <FormGroup className="form__group">
                    <input 
                      type="text" 
                      value={color} 
                      placeholder="Color" 
                      onChange={(e) => setColor(e.target.value)}
                    />
                    </FormGroup>
                    <FormGroup className="form__group">
                      <select>
                        <option value="ac">AC Ticket</option>
                        <option value="non-ac">Non AC Ticket</option>
                      </select>
                    </FormGroup>
                    <FormGroup className="select__group">
                      <button type="submit" className="btn find__car-btn" >Find Ticker</button>
                    </FormGroup>

                   
                  </div>
                </Form>
              </Col>
              <Col lg="3" md="3" sm="12" >
              <div className="find__cars-right" style={{width:"100%", height:'100%'}}></div>

              </Col>
            </Row>
          </Container>
        </div>
      </section>
      {/* =========== about section ================ */}
      <AboutSection />
      {/* ========== services section ============ */}
      <section>
        <Container>
          <Row>
            <Col lg="12" className="mb-5 text-center">
              <h6 className="section__subtitle">See our</h6>
              <h2 className="section__title">Popular Services</h2>
            </Col>

            <ServicesList />
          </Row>
        </Container>
      </section>
      {/* =========== car offer section ============= */}
      <section>
        <Container>
          {/* <Row>
            <Col lg="12" className="text-center mb-5">
              <h6 className="section__subtitle">Come with</h6>
              <h2 className="section__title">Hot Offers</h2>
            </Col>

            {carData.slice(0, 6).map((item) => (
              <CarItem item={item} key={item.id} />
            ))}
          </Row> */}
        </Container>
      </section>
      {/* =========== become a driver section ============ */}
      <BecomeOurCustomer />

      {/* =========== testimonial section =========== */}
      <section>
        <Container>
          <div style={{marginBottom:'2%'}}></div>
          <Row>
            <Col lg="12" className="mb-4 text-center">
              <h6 className="section__subtitle">Our clients says</h6>
              <h2 className="section__title">Testimonials</h2>
            </Col>

            <Testimonial />
          </Row>
        </Container>
      </section>

      {/* =============== blog section =========== */}
      <section>
        <Container>
          <Row>
            <Col lg="12" className="mb-5 text-center">
              <h6 className="section__subtitle">Explore our blogs</h6>
              <h2 className="section__title">Latest Blogs</h2>
            </Col>

            <BlogList />
          </Row>
        </Container>
      </section>
    </Helmet>
  );
};

export default HomePage;