export const data = [
  // Histock là người đứng đầu (không có cấp trên)
  [
    {
      v: "Histock",
      f: 'Histock<div style="color:red; font-style:italic; font-size:32px">President</div>',
    },
    "", // Không có cấp trên
    "The President",
  ],
  
  // Các phòng ban trực thuộc Histock
  [
    {
      v: "IT Department",
      f: 'IT Department<div style="color:blue; font-style:italic">Head of IT</div>',
    },
    "Histock", // Phòng IT trực thuộc Histock
    "Head of IT",
  ],
  [
    {
      v: "HR Department",
      f: 'HR Department<div style="color:green; font-style:italic">Head of HR</div>',
    },
    "Histock", // Phòng HR trực thuộc Histock
    "Head of HR",
  ],
  [
    {
      v: "Product Department",
      f: 'Product Department<div style="color:purple; font-style:italic">Head of Product</div>',
    },
    "Histock", // Phòng Product trực thuộc Histock
    "Head of Product",
  ],

  // Phòng ban tư vấn chuyên môn
  [
    {
      v: "Advisor Department",
      f: 'Advisor Department<div style="color:orange; font-style:italic">Head of Consulting</div>',
    },
    "Histock", // Advisor Department trực thuộc Histock
    "Head of Consulting",
  ],

  // Các vị trí trong Advisor Department
  ["Technology Advisor", "Advisor Department", ""],
  ["Financial Advisor", "Advisor Department", ""],

  // Các vị trí trong IT Department
  ["Frontend Developer", "IT Department", ""],
  ["Backend Developer", "IT Department", ""],
  ["AI Engineer", "IT Department", ""],
  ["Data Scientist", "IT Department", ""],

  // Các vị trí trong Product Department
  ["Product Manager", "Product Department", ""],
  ["Designer", "Product Department", ""],
  ["Research Assistant (Product)", "Product Department", ""],

  // Các vị trí trong HR Department
  ["Research Assistant (HR)", "HR Department", ""],
];
