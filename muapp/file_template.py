from .models import clothes

def readURL():
    clothes_info = clothes.object.all()
    if clothes_info:
        clothes_info = clothes.object.all().order_by('-upload_date')[0] #최근 파일
        

    # function readURL(input) {
    # if (input.files && input.files[0]) {

    #     var reader = new FileReader();

    #     reader.onload = function(e) {
    #     $('.image-upload-wrap').hide();

    #     $('.file-upload-image').attr('src', e.target.result);
    #     $('.file-upload-content').show();

    #     $('.image-title').html(input.files[0].name);
    #     };

    #     reader.readAsDataURL(input.files[0]);

    # } else {
    #     removeUpload();
    # }
    # }

def removeUpload():
    # function removeUpload() {
    # $('.file-upload-input').replaceWith($('.file-upload-input').clone());
    # $('.file-upload-content').hide();
    # $('.image-upload-wrap').show();
    # }
    # $('.image-upload-wrap').bind('dragover', function () {
    #     $('.image-upload-wrap').addClass('image-dropping');
    # });
    # $('.image-upload-wrap').bind('dragleave', function () {
    #     $('.image-upload-wrap').removeClass('image-dropping');
    # });











    =================================================
<!-- file upload template start-->
                                <script class="jsbin" src="https://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
                                <div class="file-upload">
                                  {% comment %} 
                                  <button class="file-upload-btn" type="button" onclick="{{$('.file-upload-input').trigger( 'click' )}}">Add Image</button> 
                                  - onclick에 file-upload-input을 클릭하는 기능을 할 수 있게 구현
                                  {% endcomment %}
                                  <button class="file-upload-btn" type="button" onclick="">Add Image</button>
                                
                                  {% comment %} 
                                  만약 파일이 올라가면 
                                  1. image-upload-wrap(올리기 대기)는 숨기기 
                                  2. file-upload-image(이미지) 띄우기
                                  3. file-upload-content(올린 내용)은 띄우기
                                  4. image-title(이미지명) 띄우기
                                  {% endcomment %}

                                  <div class="image-upload-wrap">
                                    {% comment %} 
                                    <input class="file-upload-input" type='file' onchange="{{readURL(this);}}" accept="image/*" /> 
                                    - onchange에 사진이랑 파일명 띄우는 기능 구현예정
                                    {% endcomment %}
                                    <input class="file-upload-input" type='file' onchange="" accept="image/*" multiple="multiple" />
                                    
                                    <div class="drag-text">
                                      <h3>Drag and drop a file or select add Image</h3>
                                    </div>
                                  </div>
                                  <div class="file-upload-content">
                                    <img class="file-upload-image" src="#" alt="your image" />
                                    <div class="image-title-wrap">
                                      {% comment %} 
                                      <button type="button" onclick="{{removeUpload()}}" class="remove-image">Remove <span class="image-title">Uploaded Image</span></button> 
                                      
                                      {% endcomment %}
                                      <button type="button" onclick="" class="remove-image">Remove <span class="image-title">Uploaded Image</span></button>
                                    
                                    </div>
                                  </div>
                                </div>
                                <!-- file upload template end-->         