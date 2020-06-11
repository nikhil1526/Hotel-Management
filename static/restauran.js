if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', ready)
} else {
    ready()
}

function ready(){

	var buton=document.getElementById('b')
	buton.addEventListener('click',Add)

	// var change=document.getElementsByClassName('c')
	// for(var i=0;i<change.length;i++){
	// 	var but=change[i]

	// 	but.addEventListener('click',Change)
	// }

}

function Add(event){
	var buton=event.target
	
	var form=document.getElementById('form')
	
	var a=form.getElementsByTagName('div')[0]
	if(a.childNodes.length>1){
		alert('Please add one item at a time')
	}
	else{


	
	
	var element=`
	<label for="title">Name</label>
	
	
	<input type='text' id='title' name='title' label='Name' required>
	<label for="price">Price</label>
	<input type='number' id='price' name='price' label='Price' required>
	<span>Type</span>
	<select name='type'>
	<option value="Vegetarian">Vegetarian</option>
	<option value="Non-Vegetarian">Non-Vegetarian</option>
	<option value="Bread">Bread</option>
	<option value="Chinese">Chinese</option>
	<option value="Soup">Soup</option>
	<option value="Dessert">Dessert</option>
	</select>
	<button type="submit" class="btn btn-primary">Add</button>
	`
	a.innerHTML=element
	}
	
	


}

function Change(button,item,price_is,type){

var element=button.parentElement
var allspans=document.getElementsByClassName('changes')
var span=element.getElementsByClassName('changes')[0]
var index=Number(-1)
for(var i=0;i<allspans.length;i++){
	if(allspans[i]==span){
		index=i;
		break;
	}

}
index=index+1
index=String(index)
var idis="my_form_"+index
console.log(idis)

price=Number(price_is)
new_element=`
<button name="change" type="submit" class="btn btn-primary" form=${idis}>
	Update Price
	
</button>`
element.childNodes[1].remove()

span.innerHTML=new_element

var previous=element.parentElement


previous.childNodes[7].childNodes[0].remove()
new_element=`
<input type='number' id='price' form=${idis} name='price' value=${price} label='Price' required>`

previous.childNodes[7].innerHTML=new_element

previous.childNodes[13].childNodes[1].childNodes[3].remove()








}