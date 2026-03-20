import "@typespec/http";
import "@typespec/rest";

using TypeSpec.Http;

@service({ title: "Library Service" })
namespace Library;

model Book {
  id: int32;
  title: string;
}

@route("/books")
interface Books {
  @get list(): Book[];
}