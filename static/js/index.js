import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.118/build/three.module.js";
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.118/examples/jsm/controls/OrbitControls.js';
import { OBJLoader } from "https://cdn.jsdelivr.net/npm/three@0.118/examples/jsm/loaders/OBJLoader.js";
import { MTLLoader } from 'https://cdn.jsdelivr.net/npm/three@0.118.3/examples/jsm/loaders/MTLLoader.js';


const w = window.innerWidth;
const h = window.innerHeight;
const scene = new THREE.Scene();
//辅助线
// var axes=new THREE.AxesHelper(100);
// scene.add(axes);

const camera = new THREE.PerspectiveCamera(75, w / h, 0.1, 1000);
camera.position.z = 5;
// const renderer = new THREE.WebGLRenderer();

const renderer = new THREE.WebGLRenderer({
  antialias: true,
  alpha: true
});
renderer.setSize(window.innerWidth,window.innerHeight);
// renderer.setClearColor(0x222222,0)
//色彩空间渲染方式
renderer.outputEncoding = THREE.sRGBEncoding;
renderer.textureEncoding = THREE.sRGBEncoding;
//开启渲染阴影
renderer.shadowMap.enabled = true;
renderer.hadowMapEnabled = true;

document.body.appendChild(renderer.domElement);


const controls = new OrbitControls(camera, renderer.domElement);
controls.update();

const light = new THREE.AmbientLight(0xcccccc,0.4); 
// const light = new THREE.AmbientLight(0x000000,0.4);
scene.add( light );
const pointlight=new THREE.PointLight(0xffffff,0.8);
camera.add(pointlight);

function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}



// const loader = new OBJLoader();
// loader.load("./assets/models/demo.obj", (obj) => init(obj.children[0].geometry) );

// const loader = new OBJLoader();
// loader.load("./assets/0308/mesh_medpoly.obj", (obj) => init(obj.children[0].geometry) );

/**
 * OBJ和材质文件mtl加载
 */
// var objLoader = new THREE.ObjectLoader();
// var mtlLoader = new THREE.MTLLoader();//材质文件加载器
// mtlLoader.load('./assets/0308/mesh_medpoly.mtl', function(materials) {
//   // 返回一个包含材质的对象MaterialCreator
//   console.log(materials);
//   //obj的模型会和MaterialCreator包含的材质对应起来
//   objLoader.setMaterials(materials);
//   objLoader.load('./assets/0308/mesh_medpoly.obj', function(obj) {
//   console.log(obj);
//   obj.scale.set(10, 10, 10); //放大obj组对象
//   scene.add(obj);//返回的组对象插入场景中
//   })
// })

// 加载模型
let manager = new THREE.LoadingManager();
new MTLLoader(manager)
.setPath("../static/models/demo/")
  .load("mesh_medpoly.mtl", (materials) => {
    console.log(manager);
    materials.preload();
    new OBJLoader(manager)
      .setMaterials(materials)
      .load("../static/models/demo/mesh_medpoly.obj", (obj) => {
        scene.add(obj);
        animate();
      });
  });


function handleWindowResize () {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}
window.addEventListener('resize', handleWindowResize, false);