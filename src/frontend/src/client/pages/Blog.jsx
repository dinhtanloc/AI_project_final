import React from "react";
import { Container, Row } from "reactstrap";
import Helmet from "@client/components/Helmet/Helmet";
import CommonSection from "@client/components/UI/CommonSection";
import BlogList from "@client/components/UI/BlogList";

const Blog = () => {
  return (
    <Helmet title="Blogs">
      <CommonSection   title="Blogs" />
      <section style={{backgroundColor:'#fff'}}>
        <Container >
          <Row>
            <BlogList/>
            {/* <BlogList /> */}
          </Row>
        </Container>
      </section>
    </Helmet>
  );
};

export default Blog;
