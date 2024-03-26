from django.test import TestCase

 # Create your tests here.


# {% extends "base.html" %}
# {% load static %}



# {% block header %}
# {% include "inc/navbar.html" %}
# {% endblock header %}


# {% block content %}
# <style>

# /* CSS */
# .button-31 {
#   background-color: #222;
#   border-style: none;
#   color: #fff;
#   cursor: pointer;
#   font-family: "Farfetch Basis","Helvetica Neue",Arial,sans-serif;
#   font-size: 12px;
#   font-weight: 700;
#   margin: 0;
#   max-width: none;
#   min-width: 10px;
#   outline: none;
#   overflow: hidden;
#   padding: 9px 20px 8px;
#   position: relative;
#   text-align: center;
# }

# .button-31:hover,
# .button-31:focus {
#   opacity: .75;
# }


# </style>
# <main class="main">
#      <!-- Breadcrumb Begin -->
#      <div class="breadcrumb-option">
#         <div class="container">
#             <div class="row">
#                 <div class="col-lg-12">
#                     <div class="breadcrumb__links">
#                         <a href="/"><i class="fa fa-home"></i> Home</a>
#                         <a href="/"><i class="fa fa-cart"></i> Shopping cart</a>
#                         <span>Checkout</span>
#                     </div>
#                 </div>
#             </div>
#         </div>
#     </div>
#     <!-- Breadcrumb End -->


  
#     <div class="page-content">
#       <div class="cart mb-5">
#         <div class="container">
#           <div class="row">
            
           
#             <div class="col-md-8 cart-item-box">
#               {% comment %} <h5 class="text-dark mb-3">1. &nbsp; Select a delivery address</h5> {% endcomment %}
                  
#               {% if addresses %}
              
#                   <a href="/checkout_add_address/">
#                       <div class="d-flex justify-content-end mr-3">
#                           <button type='button' class="btn btn-dark" id="addAddressBtn">Add New Address</button>
#                       </div>
#                   </a>
#                   <form method="post" action="{% url "place_order" %}" enctype="multipart/form-data">
#                     {% csrf_token %}
#                   {% comment %} <form method="post" id="addressForm"> {% endcomment %}
#                     <div class="address-container" >
#                         <label for="selected_address">Choose a delivery address:</label>
#                         {% if messages %}
#                     <ul class="messages  " style="list-style: none; color:red">
#                         {% for message in messages %}
#                             <li {% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
#                         {% endfor %}
#                     </ul>
#                 {% endif %}
#                         <ul style="list-style: none;">
#                           {% for address in addresses %}
#                             <li style="border: 1px solid #333; margin: 10px; padding: 20px; color: black;">
#                               <input type="radio" name="selected_address" id="address_{{ address.id }}" value="{{ address.id }}" {% if forloop.last %}checked{% endif %} required>
#                               <label for="address_{{ address.id }}">
#                                 <span style="font-weight: bold;">Address {{ address.counter }}:</span>
#                                 <br>
#                                 {{ address.name }}<br>
#                                 {{ address.number }}<br>
#                                 {{ address.address }}, {{ address.city }}, {{ address.state }}, {{ address.pincode }}
#                               </label>
#                             </li>
#                           {% endfor %}
#                         </ul>
#                       </div>
#               {% else %}

#                   <!-- Display add address button with an image when there are no addresses -->
#                   <div class="text-center">
#                     <img src="{% static 'main/shirt2.3.jpg' %}" alt="No Address Image" style="height: 35rem; display: block; margin: 0 auto;display: flex; justify-content: end; align-items: center;">
#                     <p>No addresses available. Add a new address.</p>
#                     <a href="/checkout_add_address/">
#                         <button type="button" class="btn btn-dark" id="addAddressBtn">Add New Address</button>
#                     </a>
#                 </div>
                
#               {% endif %}
          
#             </div><!-- End .col-lg-9 -->
              



# <!-- side start--> 
#             <div class="col-lg-4">
#                 <div class="coupon">
#                     <input type="text" name="code" class="form-control m-2" id="couponCode" placeholder="Enter coupon code"   >
#                   <div class="d-flex justify-content-end mb-3" >
#                     <button style="margin-right: 7px;" class="btn btn-light" type="button"  data-toggle="modal" data-target="#couponModal">Available Coupons</button>
#                     <button id="applyCouponBtn" style="margin-right: 7px;" class="button-31" type="submit" >Apply</button>
#                     <a href="/remove_coupen/"><button class="bg-danger button-31 removeCouponBtn" role="button">Remove</button> </a>
                    
#                   </div> 
#                 </div>
                
#                         <!-- Bootstrap Modal -->
#                         <div class="modal fade" id="couponModal" tabindex="-1" role="dialog" aria-labelledby="couponModalLabel" aria-hidden="true">
#                           <div class="modal-dialog" role="document">
#                             <div class="modal-content p-5 mar">
#                               <div class="modal-header">
#                                 <h5 class="modal-title" id="couponModalLabel">Available Coupons</h5>
#                                 <button type="button" class="close" data-dismiss="modal" aria-label="Close">
#                                   <span aria-hidden="true">&times;</span>
#                                 </button>
#                               </div>
#                               <div class="modal-body">
#                                 <!-- Dummy Data for Coupons -->
#                                 <ul>
#                                   {% if coupons %}
#                                     {% for c in coupons %}
#                                     <li style="display: flex; flex-direction: column; background-color: #fffff0; padding: 10px; margin-bottom: 15px;">
#                                       <span style="font-weight: bold; color: #ff9900; font-size: 18px;"></span>
#                                       <span style="font-weight: bold; color: #ff9900; font-size: 16px;"> Coupon Code :  {{ c.code }} </span>
#                                       <span style="color: #666; font-size: 14px;">Minimum Purchase: &#8377; {{ c.min_amount }}</span>
#                                       <span style="color: #666; font-size: 14px;">Expiry Date: {{ c.end_date }}</span>
#                                     </li>
#                                     {% endfor %}
#                                   {% else %}
#                                     No Coupon Available...
#                                   {% endif %}
#                                 </ul>
#                               </div>
#                             </div>
#                           </div>
#                         </div>

                        
#                 <div class="checkout__order">
#                     <h5>Your order</h5>
#                     <div class="checkout__order__product">
#                         <ul>
#                             <li>
#                                 <span class="top__text">Product</span>
#                                 <span class="top__text__right">Total</span>
#                             </li>
#                             {% for i in cart_items  %}
#                             <li>01. {{ i.size_variant }} <span>$ {{ i.pro_total }}</span></li>
                            
#                             {% endfor %}
#                         </ul>
#                     </div>
#                     <div class="checkout__order__total">
#                         <ul>
#                             <li>Subtotal <span>$ {{ sub_total1 }}</span></li>
#                             <li>Total <span>$ {{ sub_total1 }}</span></li>
#                         </ul>
#                     </div>
                
#                     <div class="checkout__order__widget">
#                         <label for="payment-option" >Choose a payment option:</label>
#                         <input type="hidden" id="total_amount" name="sub_total" value="{{ sub_total1 }}">

#                         <div class="payment-options">
#                           <div class="col-md-6 mb-3">

#                             <input type="hidden" name="payment_option" value="cod">
#                             <button type="submit" class="btn btn-danger btn-block">COD</button>
#                         </div>
#                         <div class="col-md-6 mb-3">
#                           <button type="submit" class="btn btn-danger btn-block">Wallet</button>
#                       </div>
#                       <div class="col-md-6 mb-3">
#                         <button type="button" id="rzp-button1" class="btn btn-danger btn-block razor">Razorpay</button>
#                     </div>
#                         </div>
#                       </div>
#                   </div>
#                 </form>
#               </div>
#             </div>
#           </div><!-- End .row -->
#         </div><!-- End .container -->
#       </div><!-- End .cart -->
#     </div><!-- End .page-content -->
#   </main><!-- End .main -->




# <!-- rzp-button1 -->
# <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
# <script src="https://code.jquery.com/jquery-3.6.4.min.js"></script>



#  <!--razor-pay scripts -->

# <script>

#   $(document).ready(function (){

#     $('.razor').click(function (e){
#         e.preventDefault();
#         var selectedValue = $('input[name="selected_address"]:checked').val();
#         var token = $('input[name=csrfmiddlewaretoken]').val();
#         var totalAmount = $('#total_amount').val();

        
        
#         console.log('Total Amount:', totalAmount); 
# console.log('hi')

#   var options = {
#       "key": "rzp_test_kjPVyHrg75EHqw",
#       "amount": "{{ payment.amount }}",
#       "currency": "INR",
#       "name": "Ashion",
#       "description": "Test Transaction",
#       "image": "https://example.com/your_logo",
#       "order_id": "{{ payment.id }}", 
#      // "callback_url": "https://eneqd3r9zrjok.x.pipedream.net/",
#       "handler": function (response){
#         if (response.razorpay_payment_id){
#           $.ajax({
#             method : 'POST',
#             url: '/razorpay_payment/',
#             data: {
#               address : selectedValue,
#               csrfmiddlewaretoken:token,
#               total_amount : totalAmount
#                   },
#           success : function (data){
#               window.location.href = data.redirect_url + data.order_id;   
#               }
#           });
#         }
#         else{
#             alert("payment failed")
#         }
        
#       },
#       "prefill": {
#           "name": "Gaurav Kumar",
#           "email": "gaurav.kumar@example.com",
#           "contact": "9000090000"
#       },
#       "theme": {
#           "color": "#cc3333"
#       }
#   };
  
#   console.log("Script executed" );
#   var rzp1 = new Razorpay(options);
#   rzp1.on('payment.success', function (response){
#     console.log("Payment success");
#           alert(response.error.reason);
          
#   });
#   document.getElementById('rzp-button1').onclick = function(e){
#       rzp1.open();
#       e.preventDefault();
#   }

#   });
# });


#   </script>


  


# {% endblock content %}





        
#         <!-- Instagram Begin -->
#        {% block instagram %}
#        {% include "inc/instagram.html" %}
#        {% endblock instagram %}
#         <!-- Instagram End -->

#         <!-- Footer Section Begin -->
#         {% block footer %}
#         {% include "inc/footer.html" %}
#         {% endblock footer %}
#         <!-- Footer Section End -->
# {% comment %} 


#         <script>
#           $(document).ready(function (){

#             $('.razor').click(function (e){
#                 e.preventDefault();
#                 var selectedValue = $('input[name="address"]:checked').val();
#                 var total_prize = $('input[name="total_prize"]').val();
#                 var token = $('input[name=csrfmiddlewaretoken]').val();
        
#                         var options = {
#                             "key": "rzp_test_ja90f2UETSDOKd",
#                             "amount": total_prize * 100, 
#                             "currency": "INR",
#                             "name": "Shoezy",
#                             "description": "Thank you for buying from us ",
#                             "image": "https://imgs.search.brave.com/EF6YntA6IJLW85LIWBz8pQfw5BpeNOdleik58EunoJs/rs:fit:500:0:0/g:ce/aHR0cHM6Ly9keW5h/bWljLmJyYW5kY3Jv/d2QuY29tL2Fzc2V0/L2xvZ28vZjgzODFi/NjQtZGRmZC00MDI4/LWE3MDUtNDdkOTc3/ZGQzNzhhL2xvZ28t/c2VhcmNoLWdyaWQt/MXg_bG9nb1RlbXBs/YXRlVmVyc2lvbj0x/JnY9NjM4MzAxOTEz/Nzk5NDAwMDAw.jpeg",
                
#                             "handler": function (response1){
#                                     if (response1.razorpay_payment_id){
#                                         $.ajax({
#                                             method : 'POST',
#                                             url: '/razor_pay/',
#                                             data: {
#                                                 'address': selectedValue,
#                                                 csrfmiddlewaretoken:token
        
#                                                     },
#                                             success : function (data){
#                                                 window.location.href = data.redirect_url  + data.order_id1;
#                                         }
#                                     });
#                                 }
#                                 else{
#                                     alert("payment failed")
#                                 }
        
#                             },
#                             "prefill": {
#                                 "name": 'name', 
#                                 "email": "sample123@gmail.com", 
#                                 "contact": 9876543219 , 
#                             },
#                             "theme": {
#                                 "color": "#3399cc"
#                             }
#                         };
#                           var rzp1 = new Razorpay(options);
#                         rzp1.open();
               
#             });
#         });
#         </script> {% endcomment %}