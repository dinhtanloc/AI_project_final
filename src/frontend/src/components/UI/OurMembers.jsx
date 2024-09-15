import React from "react";
import "@styles/our-member.css";
import { Col } from "reactstrap";
import { Link } from "react-router-dom";
import ava01 from "/media/member/Loc_Dinh.jpg";
import ava02 from "/media/member/Chi_Tran.png";
import ava03 from "/media/member/Huong_Nguyen.png";
import ava04 from "/media/member/Ngoc_Le.png";
import ava05 from "/media/member/Phat_Nguyen.png";
import Slider from "react-slick";

const OUR__MEMBERS = [
  {
    name: "Loc Tan Dinh",
    experience: "IT Department Header",
    fbUrl: import.meta.env.VITE_FACEBOOK,
    instUrl: "#",
    twitUrl: "#",
    linkedinUrl: import.meta.env.VITE_LINKEDIN,
    imgUrl: ava01,
  },

  {
    name: "Chi Tran Thi Kim",
    experience: "Project Coordinator",
    fbUrl: "#",
    instUrl: "#",
    twitUrl: "#",
    linkedinUrl: "#",
    imgUrl: ava02,
  },

  {
    name: "Huong Nguyen Thi Thanh",
    experience: "Design Manager",
    fbUrl: "#",
    instUrl: "#",
    twitUrl: "#",
    linkedinUrl: "#",
    imgUrl: ava03,
  },

  {
    name: "Ngoc Le Thi Bao",
    experience: "Market Researcher",
    fbUrl: "#",
    instUrl: "#",
    twitUrl: "#",
    linkedinUrl: "#",
    imgUrl: ava04,
  },
  {
    name: "Phat Nguyen Van",
    experience: "Research Assistant",
    fbUrl: "#",
    instUrl: "#",
    twitUrl: "#",
    linkedinUrl: "#",
    imgUrl: ava05,
  },
];

const OurMembers = () => {
  const settings = {
    dots: true,
    infinite: true,
    autoplay: true,
    speed: 1000,
    swipeToSlide: true,
    autoplaySpeed: 2000,
    slidesToShow: 4,
    slidesToScroll: 1,
    responsive: [
      {
        breakpoint: 992,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 1,
          infinite: true,
          dots: true,
        },
      },
      {
        breakpoint: 576,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
        },
      },
    ],
  };
  return (
    <Slider {...settings}>
      {OUR__MEMBERS.map((item, index) => (
        <Col lg="3" md="3" sm="4" xs="6" key={index} className="mb-4">
          <div className="single__member">
            <div className="single__member-img">
              <img src={item.imgUrl} alt="" className="w-100" />

              <div className="single__member-social">
                <Link to={item.fbUrl}>
                  <i className="ri-facebook-line"></i>
                </Link>
                <Link to={item.twitUrl}>
                  <i className="ri-twitter-line"></i>
                </Link>

                <Link to={item.linkedinUrl}>
                  <i className="ri-linkedin-line"></i>
                </Link>

                <Link to={item.instUrl}>
                  <i className="ri-instagram-line"></i>
                </Link>
              </div>
            </div>

            <h6 className="text-center mb-0 mt-3">{item.name}</h6>
            <p className="section__description text-center">
              {item.experience}
            </p>
          </div>
        </Col>
      ))}
    </Slider>
  );
};

export default OurMembers;
