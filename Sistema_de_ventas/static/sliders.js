(function(){
	const sliders = [...document.querySelectorAll(".producto_img")];
	const arrowNext = document.querySelector("#siguiente");
	const arrowBefore = document.querySelector("#antes");
	let value;
	arrowNext.addEventListener("click", ()=>changePosition(1));
	arrowBefore.addEventListener("click", ()=>changePosition(-1));
	function changePosition(change){
		const currentElement = Number(document.querySelector(".producto_img_show").dataset.id);
		value=currentElement;
		value+=change;
		if(value===0||value==sliders.length+1){
			value=value===0? sliders.length:1;
		}
		sliders[currentElement-1].classList.toggle("producto_img_show");
		sliders[value-1].classList.toggle("producto_img_show");
	}
})();

document.addEventListener('DOMContentLoaded', function() {
	const productoPrecio = document.getElementById('precio');
    const colorButtons = document.querySelectorAll('.boton_color');
    const talleButtons = document.querySelectorAll('.boton_talle')
    const comprarButton = document.getElementById('boton_comprar');
    const carritoIcono = document.getElementById('carrito-icono');
    const carritoModal = document.getElementById('carrito-modal');
    const cerrarModal = document.querySelector('.cerrar');
    const carritoContador = document.getElementById('carrito-contador');
    const carritoItems = document.getElementById('carrito-items');
    const carritoTotal = document.getElementById('carrito-total');
    let carrito = [];
    colorButtons.forEach(button => {
        button.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            document.querySelectorAll('.producto_img').forEach(img => {
                img.classList.remove('producto_img_show');
            });
            document.querySelector(`.producto_img[data-id="${id}"]`).classList.add('producto_img_show');
            const productoImg = document.querySelector(`.producto_img[data-id="${id}"] img`);
            const nombre = productoImg.getAttribute('alt');
            const imagen = productoImg.getAttribute('src');
            const precio = productoPrecio.getAttribute('data-precio');
            comprarButton.setAttribute('data-id', id);
            comprarButton.setAttribute('data-nombre', nombre);
            comprarButton.setAttribute('data-imagen', imagen);
            comprarButton.setAttribute('data-precio', precio);
        });
    });
    talleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const talle = this.getAttribute('data-talle');
            comprarButton.setAttribute('data-talle', talle);
        });
    });
    comprarButton.addEventListener('click', function() {
        const id = this.getAttribute('data-id');
        const nombre = this.getAttribute('data-nombre');
        const precio = parseFloat(this.getAttribute('data-precio'));
        const imagen = this.getAttribute('data-imagen');
        const talle = this.getAttribute('data-talle')
        const producto = { id, nombre, precio, imagen, talle };
        carrito.push(producto);
        actualizarCarrito();
    });
    carritoIcono.addEventListener('click', function() {
        carritoModal.style.display = 'block';
    });
    cerrarModal.addEventListener('click', function() {
        carritoModal.style.display = 'none';
    });
    window.addEventListener('click', function(event) {
        if (event.target == carritoModal) {
            carritoModal.style.display = 'none';
        }
    });
    function actualizarCarrito() {
        carritoContador.textContent = carrito.length;
        carritoItems.innerHTML = '';
        let total = 0;
        carrito.forEach(producto => {
            const item = document.createElement('div');
            item.innerHTML = `
            	<div class="carrito_contenedor">
	                <img src="${producto.imagen}" alt="${producto.nombre}" style="width: 150px; height: 150px; margin-right: 10px;">
		            <span style="margin-top: 40px;">${producto.nombre}</span>
		            <span style="margin-top: 40px; margin-left: 5px">$${producto.precio}</span>
		            <span style="margin-top: 65px; margin-left: -128px;">Talle: ${producto.talle}</span>
		        </div>
            `;
            carritoItems.appendChild(item);
            total += producto.precio;
        });
        carritoTotal.textContent = total + 1000;
    }
    document.getElementById('formulario-compra').addEventListener('submit', function(event) {
        event.preventDefault();
        const nombre_cliente = document.getElementById('nombre_cliente').value;
        const direccion = document.getElementById('direccion').value;
        if (nombre_cliente && direccion) {
            alert('Compra realizada con éxito');
            carrito = [];
            actualizarCarrito();
            carritoModal.style.display = 'none';
        } else {
            alert('Por favor, completa todos los campos');
        }
    });
});
