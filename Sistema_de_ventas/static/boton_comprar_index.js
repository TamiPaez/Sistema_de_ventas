function btn_carrito(){
    const eliminar = document.querySelector('.boton_eliminar')
    for(var i=0; i < eliminar.length; i++){
        var button = eliminar[i];
        button.addEventListener('click', eliminar_item);
    }
    const sumar = document.querySelector('#mas')
    for(var i=0; i < sumar.length; i++){
        var button = sumar[i];
        button.addEventListener('click', sumar_item);
    }
    const restar = document.querySelector('#menos')
    for(var i=0; i < restar.length; i++){
        var button = restar[i];
        button.addEventListener('click', restar_item);
    }
}
function eliminar_item(event){
    var btn_eliminar = event.target;
    btn_eliminar.parentElement.remove();
    actualizarCarrito()
}
function sumar_item(event){
    var btn_sumar = event.target;
    btn_eliminar.parentElement.remove();
    actualizarCarrito()
}
function restar_item(event){
    var btn_restar = event.target;
    btn_eliminar.parentElement.remove();
    actualizarCarrito()
}

document.addEventListener('DOMContentLoaded', function() {
    const comprarButton = document.querySelectorAll('.boton_comprar');
    const talleButtons = document.querySelectorAll('.boton_talle');
    const carritoIcono = document.getElementById('carrito-icono');
    const carritoModal = document.getElementById('carrito-modal');
    const cerrarModal = document.querySelector('.cerrar')
    const cerrarCarritoModal = document.querySelector('.cerrar-carrito');
    const carritoContador = document.getElementById('carrito-contador');
    const carritoItems = document.getElementById('carrito-items');
    const carritoTotal = document.getElementById('carrito-total');
    const modal = document.getElementById('modal-seleccion');
    const botonListo = document.getElementById('boton-listo');
    const colorButtons = document.querySelectorAll('.boton_color');
    const colorPicker = document.getElementById('color-picker-modal');
    let carrito = [];
    let producto = {};
    let talle = null;
    let color = null;

    comprarButton.forEach(button => {
        button.addEventListener('click', function() {
            const producto_img = this.closest('.producto_index');
            const id = producto_img.getAttribute('data-id');
            const nombre = producto_img.querySelector('.mover_nombre').textContent;
            const precio = parseFloat(producto_img.getAttribute('data-precio'));
            const imagen = producto_img.querySelector('img').getAttribute('src');
            producto = { id, nombre, precio, imagen };
            if (id === "2") {
                colorPicker.style.display = "block";
                document.querySelector('.modal-contenido h2').innerHTML = `Selecciona Talle y Color para <br> ${nombre}`;
            } else {
                colorPicker.style.display = "none";
                document.querySelector('.modal-contenido h2').innerHTML = `Selecciona Talle para <br> ${nombre}`;
            }
            modal.style.display = "block";
        });
    });
    talleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const talle = this.getAttribute('data-talle');
            document.querySelectorAll('.boton_talle').forEach(btn => btn.classList.remove('selected'));
            this.classList.add('selected')
            producto.talle = talle;
        });
    });
    colorButtons.forEach(button => {
        button.addEventListener('click', function() {
            const color = this.getAttribute('data-color');
            document.querySelectorAll('.boton_color').forEach(btn => btn.classList.remove('selected'));
            this.classList.add('selected')
            producto.color = color;
        });
    });

    cerrarModal.addEventListener('click', function() {
        modal.style.display = "none";
    });

    window.addEventListener('click', function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });

    botonListo.addEventListener('click', function() {
        if (producto.talle=="") {
            alert("Por favor, selecciona un talle.");
            return;
        }
        if (colorPicker.style.display === "block" && producto.color=="") {
            alert("Por favor, selecciona un color.");
            return;
        }
        carrito.push(producto);
        actualizarCarrito();
        alert("Producto agregado al carrito correctamente.");
        modal.style.display = "none";
    });
    carritoIcono.addEventListener('click', function() {
        carritoModal.style.display = 'block';
    });
    cerrarCarritoModal.addEventListener('click', function() {
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
                    
                    <div class="carrito_detalles">
                        <span style="margin-top: 30px;">${producto.nombre}</span>
                        <span style="margin-top: 10px; margin-left: 5px">$${producto.precio}</span>
                        <span style="margin-top: 10px; margin-left: 5px;">Talle: ${producto.talle}</span>
                    </div>
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
            /*
            fetch('/Divina_Amarga/compra',{
                method:'POST',
                headers:{
                    'Content-Type':'application/json'
                },
                body:JSON.stringify({carrito:carrito})
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
            
                alert('Compra realizada con éxito');
                carrito = [];
                actualizarCarrito();
                carritoModal.style.display = 'none';
            })
            .catch(error => {
                console.error('Error:', error);
        });*/
        } else {
            alert('Por favor, completa todos los campos');
        }
    });
});
